from libs import parser
from libs.utility import utils

yaml = utils.yaml_parser('knot.yml')
data_yaml = parser.initialiaze(data=yaml)
print(data_yaml)
# data_json = initialiaze(data=json_req)
# print(data_json)