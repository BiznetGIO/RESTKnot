#!/usr/bin/env python
"""An example of cursor dealing with prepared statements.

A cursor can be used as a regular one, but has also a prepare() statement. If
prepare() is called, execute() and executemany() can be used without query: in
this case the parameters are passed to the prepared statement. The functions
also execute the prepared statement if the query is the same prepared before.

Prepared statements aren't automatically deallocated when the cursor is
deleted, but are when the cursor is closed. For long-running sessions creating
an unbound number of cursors you should make sure to deallocate the prepared
statements (calling close() or deallocate() on the cursor).

"""

# Copyright (C) 2012 Daniele Varrazzo  <daniele.varrazzo@gmail.com>

import re
from threading import Lock

import psycopg2
import psycopg2.extensions as ext


class PreparingCursor(ext.cursor):
    _lock = Lock()
    _ncur = 0

    def __init__(self, *args, **kwargs):
        super(PreparingCursor, self).__init__(*args, **kwargs)
        # create a distinct name for the statements prepared by this cursor
        self._lock.acquire()
        self._prepname = "psyco_%x" % self._ncur
        PreparingCursor._ncur += 1
        self._lock.release()

        self._prepared = None
        self._execstmt = None

    _re_replargs = re.compile(r"(%s)|(%\([^)]+\)s)")

    def prepare(self, stmt):
        """Prepare a query for execution.

        TODO: handle literal %s and $s in the string.
        """
        # replace the python placeholders with postgres placeholders
        parlist = []
        parmap = {}
        parord = []

        def repl(m):
            par = m.group(1)
            if par is not None:
                parlist.append(par)
                return "$%d" % len(parlist)
            else:
                par = m.group(2)
                assert par
                idx = parmap.get(par)
                if idx is None:
                    idx = parmap[par] = "$%d" % (len(parmap) + 1)
                    parord.append(par)

                return idx

        pgstmt = self._re_replargs.sub(repl, stmt)

        if parlist and parmap:
            raise psycopg2.ProgrammingError(
                "you can't mix positional and named placeholders"
            )

        self.deallocate()
        self.execute("prepare %s as %s" % (self._prepname, pgstmt))

        if parlist:
            self._execstmt = "execute %s (%s)" % (self._prepname, ",".join(parlist))
        elif parmap:
            self._execstmt = "execute %s (%s)" % (self._prepname, ",".join(parord))
        else:
            self._execstmt = "execute %s" % (self._prepname)

        # print(f"prepared: {stmt}")
        self._prepared = stmt

    @property
    def prepared(self):
        """The query currently prepared."""
        # print(f"prepared: {self._prepared}")
        return self._prepared

    def deallocate(self):
        """Deallocate the currently prepared statement."""
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
                "execute() with no query called without prepare"
            )

        # print(f"execute: {stmt} {args}")
        return super(PreparingCursor, self).execute(stmt, args)

    def executemany(self, stmt, args=None):
        if args is None:
            args = stmt
            stmt = self._execstmt

            if stmt is None:
                raise psycopg2.ProgrammingError(
                    "executemany() with no query called without prepare"
                )
        else:
            if stmt != self._prepared:
                self.prepare(stmt)

        return super(PreparingCursor, self).executemany(self._execstmt, args)

    def close(self):
        if not self.closed and not self.connection.closed and self._prepared:
            self.deallocate()

        return super(PreparingCursor, self).close()
