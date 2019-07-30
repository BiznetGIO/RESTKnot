import os
import re
from threading import Lock
import psycopg2
import psycopg2.extensions as ext
import random
import string


def randomString(stringLength=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

class PreparingCursor(ext.cursor):
    _lock = Lock()
    _ncur = 0
    def __init__(self, *args, **kwargs):
        super(PreparingCursor, self).__init__(*args, **kwargs)
        self._lock.acquire()
        random_string = randomString()
        self._prepname = "psyco{}_{}".format(str(random_string), self._ncur)
        PreparingCursor._ncur += 1
        self._lock.release()

        self._prepared = None
        self._execstmt = None

    _re_replargs = re.compile(r'(%s)|(%\([^)]+\)s)')

    def prepare(self, stmt):
        parlist = []
        parmap = {}
        parord = []
        
        def repl(m):
            par = m.group(1)
            if par is not None:
                parlist.append(par)
                return "${}".format_map(len(parlist)) 
            else:
                par = m.group(2)
                assert par
                idx = parmap.get(par)
                if idx is None:
                    idx = parmap[par] = "${}".format(len(parmap) + 1)
                    parord.append(par)

                return idx

        pgstmt = self._re_replargs.sub(repl, stmt)
        if parlist and parmap:
            raise psycopg2.ProgrammingError(
                "you can't mix positional and named placeholders")

        self.deallocate()
        self.execute("prepare {} as {}".format(self._prepname, pgstmt))

        if parlist:
            self._execstmt = "execute {} ({})".format(
                self._prepname, ','.join(parlist))
        elif parmap:
            self._execstmt = "execute {} ({})".format(
                self._prepname, ','.join(parord))
        else:
            self._execstmt = "execute {}".format(self._prepname)
        self._prepared = stmt

    @property
    def prepared(self):
        return self._prepared

    def deallocate(self):
        if self._prepared is not None:
            self.execute("deallocate " + self._prepname)
            self._prepared = None
            self._execstmt = None

    def execute(self, stmt=None, args=None):
        if stmt is None or stmt == self._prepared:
            stmt = self._execstmt
        elif not isinstance(stmt, str):
            args = stmt
            stmt = self._execstmt

        if stmt is None:
            raise psycopg2.ProgrammingError(
                "execute() with no query called without prepare")
        return super(PreparingCursor, self).execute(stmt, args)

    def executemany(self, stmt, args=None):
        if args is None:
            args = stmt
            stmt = self._execstmt

            if stmt is None:
                raise psycopg2.ProgrammingError(
                    "executemany() with no query called without prepare")
        else:
            if stmt != self._prepared:
                self.prepare(stmt)

        return super(PreparingCursor, self).executemany(self._execstmt, args)

    def close(self):
        if not self.closed and not self.connection.closed and self._prepared:
            self.deallocate()

        return super(PreparingCursor, self).close()
