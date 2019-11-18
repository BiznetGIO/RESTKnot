import json

from dnsagent.clis.base import Base
from dnsagent.libs import knot as knot_lib
from dnsagent.libs import utils


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
        utils.check_root()
        if self.args["start"]:
            data = self.args["--data"]
            knot_lib.begin()
            json_data = json.loads(data)
            try:
                result = knot_lib.libknot_json(json_data)["data"]
            except Exception as e:
                utils.log_err(str(e))
            else:
                results = json.loads(result)
                for i in results:
                    print(results[i])
            knot_lib.commit()
            exit()

        if self.args["load"]:
            path = self.args["--file"]
            json_data = utils.yaml_parser_file(path)
            knot_lib.begin()
            for i in json_data:
                try:
                    result = knot_lib.libknot_json(i)["data"]
                except Exception as e:
                    utils.log_err(str(e))
                else:
                    results = json.loads(result)
                    for i in results:
                        print(results[i])
            knot_lib.commit()
            exit()
