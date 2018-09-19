from libs import utils
from libs.command import action
import json


# Json_req Hapus Setelah jadi
json_req = {
  "configbegin": {
    "sendblock": {
      "cmd": "conf-begin"
    },
    "receive": {
      "type": "block"
    }
  },
  "configset": {
    "sendblock": {
      "cmd": "conf-set",
      "section": "zone",
      "item": "domain",
      "data": "tes123"
    },
    "receive": {
      "type": "block"
    }
  },
  "configcommit": {
    "sendblock": {
      "cmd": "conf-commit"
    },
    "receive": {
      "type": "block"
    }
  },
  "statsserver": {
    "sendblock": {
      "cmd": "stats"
    },
    "receive": {
      "type": "stats"
    }
  }
}


def check_command(command):
    sdl_data = utils.repodata()
    try:
        sdl_data[command]
    except Exception as e:
        print("illigal command : ", e)
    else:
        return True

def check_parameters(command,parameters):
    sdl_data = utils.repodata()
    try:
        sdl_data[command]['parameters'][parameters]
    except Exception as e:
        print("illegal parameter : ",e)
    else:
        return True

def parser(yaml):
    projec_obj = list()
    for project in yaml: # ambil index project
        action_obj = list()
        for action in yaml[project]: # ambil index aksi
            if not check_command(action):
                return None
            else:
                data_obj = dict()
                for params in yaml[project][action]: # ambil index parameter
                    if not check_parameters(action,params):
                        return None
                    else:
                        data_obj[params]=yaml[project][action][params]
                action_obj.append({
                    action: data_obj
                })
        projec_obj.append({
            project: action_obj
        })
    return projec_obj


def initialiaze(data=None):
    try:
        parser_data = parser(data)
    except Exception:
        print("Error: Parameter data Needed")
    else:
        return parser_data

yaml = utils.yaml_parser('knot.yml')
data_yaml = initialiaze(data=yaml)
print(data_yaml)
# data_json = initialiaze(data=json_req)
# print(data_json)


