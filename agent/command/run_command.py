from command.parser import parser
from command.utility import utils

while True:
    print("-----------------------------------------")
    print("TEMPLATES COMMAND : ")
    print("-----------------------------------------")
    list_dirs = utils.list_dir("test/templates/")
    no = 1
    yaml_file = None
    data_choose = list()
    for vldir in list_dirs:
        templates = vldir.split("/")
        templates = templates[2]
        print(str(no)+" | "+templates)
        templates_name = templates.split(".")
        templates_name = templates_name[0]
        data = {
            "name": templates_name,
            "file": vldir,
            "choose": no
        }
        data_choose.append(data)
        no = no+1
    print("-----------------------------------------")
    print("0 | Exit")
    print("-----------------------------------------")

    choose = input("Select Your Command : ")
    if choose == 0:
        print("Thank You")
        exit()
    else:
        print("Executing")
        for command in data_choose:
            if command['choose'] == choose:
                yaml_file = command['file']
        yaml_data = utils.yaml_parser(yaml_file)
        data_yaml = parser.initialiaze(data=yaml_data)
        a = parser.execute_command(data_yaml)
        print(a)


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