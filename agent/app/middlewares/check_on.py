import os, json
from app.libs import utils
from command import read_rest


master_ip = os.environ.get("MASTER_HOST", os.getenv("MASTER_HOST"))
nm_host = os.environ.get("NAME_HOST", os.getenv("NAME_HOST"))
master_port = os.environ.get("MASTER_PORT", os.getenv("MASTER_PORT"))
status_agent = os.environ.get("STATUS_AGENT", os.getenv("STATUS_AGENT"))
url = "http://"+str(master_ip)+":"+str(master_port)+"/api/agent/check"


def check_on_server():
    json_read = {
        "zone-read": {
            "sendblock": {
                "cmd": "conf-read",
                "section": "zone",
                "item": "domain"
            },
            "receive": {
                "type": "block"
            }
        }
    }
    data_zone = None
    try:
        data_zone = read_rest(json_read)['data']
    except Exception as e:
        print(e)
    else:
        zone_send = list()
        try:
            data_zone = json.loads(data_zone)['zone']
        except Exception as e:
            data_zone = {}
        else:
            for i in data_zone:
                zone_send.append(i[:-1])
            
            data = {
                "nm_host": nm_host,
                "status_agent": status_agent,
                "data_zone": zone_send
            }
            try:
                response = utils.send_http(url, data)
            except Exception as e:
                print(e)
            else:
                print(response)

def refreshZone():
    json_read = {
        "zone-read": {
            "sendblock": {
                "cmd": "zone-refresh"
            },
            "receive": {
                "type": "block"
            }
        }
    }
    try:
        data = read_rest(json_read)
    except Exception as e:
        print(e)
    else:
        print("Zone Refresh")