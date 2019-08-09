from domba.clis.base import Base
from domba.libs import knot_lib
import os, json

class Command(Base): 
    """
        usage:
            command load [-f FILE]
            command start [-d DATA]

        Command:

        Options:
        -d data --data=DATA                   Load JSON String Format
        -f file --file=FILE                   Load YAML FROM FILE
        -h --help                             Print usage
    """
    def execute(self):
        knot_lib.utils.check_root()
        if self.args['start']:
            data = self.args['--data']
            knot_lib.begin()
            json_data = json.loads(data)
            try:
                result = knot_lib.libknot_json(json_data)['data']
            except Exception as e:
                knot_lib.utils.log_err(str(e))
            else:
                results = json.loads(result)
                for i in results:
                    print(results[i])
            knot_lib.commit()
            exit()

        if self.args['load']:
            path = self.args['--file']
            json_data = knot_lib.utils.yaml_parser_file(path)
            knot_lib.begin()
            for i in json_data:
                try:
                    result = knot_lib.libknot_json(i)['data']
                except Exception as e:
                    knot_lib.utils.log_err(str(e))
                else:
                    results = json.loads(result)
                    for i in results:
                        print(results[i])
            knot_lib.commit()
            exit()
        