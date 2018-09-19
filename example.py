from libs import parser
from libs.utility import utils

yaml = utils.yaml_parser('knot.yml')
data_yaml = parser.initialiaze(data=yaml)
print(data_yaml)

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