from libs.parsing import parser
from libs.utility import utils
# from libs.control import action

# action.load_libknot("libknot.so.7")
# action.load_sock("/var/run/knot/knot.sock")

yaml = utils.yaml_parser('command.yml')
data_yaml = parser.initialiaze(data=yaml)
parser.execute_command(data_yaml)

# HTTP REQUEST
# json_req={
#   "configbegin": {
#     "sendblock": {
#       "cmd": "conf-begin"
#     },
#     "receive": {
#       "type": "block"
#     }
#   },
#   "configset": {
#     "sendblock": {
#       "cmd": "conf-set",
#       "section": "zone",
#       "item": "domain",
#       "data": "tes123"
#     },
#     "receive": {
#       "type": "block"
#     }
#   },
#   "configcommit": {
#     "sendblock": {
#       "cmd": "conf-commit"
#     },
#     "receive": {
#       "type": "block"
#     }
#   }
# }
# data_json = parser.initialiaze(data=json_req)
# print(data_json)