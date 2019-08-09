from domba.clis.base import Base
from domba.libs import knot_lib
import os, json

class Zone(Base): 
    """
        usage:
            zone load [-f FILE] [-z ZONE]
            zone start [-d DATA] [-z ZONE]
            zone show [-z ZONE]

        Command:

        Options:
        -d data --data=DATA                   Load JSON String Format
        -f file --file=FILE                   Load YAML FROM FILE
        -z zone --zone=ZONE                   Zone or Domain name
        -h --help                             Print usage
    """
    def execute(self):
        knot_lib.utils.check_root()
        if self.args['start']:
            zone = self.args['--zone']
            if not zone:
                knot_lib.utils.log_err("Zone Or Domain Required")
                exit()
            data = self.args['--data']
            knot_lib.begin(zone)
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
            zone = self.args['--zone']
            if not zone:
                knot_lib.utils.log_err("Zone Or Domain Required")
                exit()
            path = self.args['--file']
            json_data = knot_lib.utils.yaml_parser_file(path)
            knot_lib.zone_begin()
            for i in json_data:
                try:
                    result = knot_lib.libknot_json(i)['data']
                except Exception as e:
                    knot_lib.utils.log_err(str(e))
                else:
                    results = json.loads(result)
                    for i in results:
                        print(results[i])
            knot_lib.zone_commit(zone)
            exit()
        
        if self.args['show']:
            zone = self.args['--zone']
            if not zone:
                json_data = {
                    "conf-read": {
                            "sendblock": {
                            "cmd": "zone-read",
                            "zone": ""
                        },
                        "receive": {
                            "type": "block"
                        }
                    }
                }
            else:
                json_data = {
                    "conf-read": {
                            "sendblock": {
                            "cmd": "zone-read",
                            "zone": zone
                        },
                        "receive": {
                            "type": "block"
                        }
                    }
                }
            try:
                result = knot_lib.libknot_json(json_data)['data']
            except Exception as e:
                knot_lib.utils.log_err(str(e))
            else:
                results = json.loads(result)
                for i in results:
                    print(results[i])
            
            