import requests
import json
import os
import logging
import coloredlogs

url_boot = os.environ.get("HOST", "127.0.0.1")
port_boot = os.environ.get("PORT", "6967")

urls = "http://"+url_boot+":"+port_boot+"/api/bootstrap"
urls_knot = "http://"+url_boot+":"+port_boot+"/api/command_rest"
print(urls_knot)

def log_rep(stdin):
    coloredlogs.install()
    logging.info(stdin)

def log_err(stdin):
    coloredlogs.install()
    logging.error(stdin)

def send_http(url, data, headers=None):
    json_data = json.dumps(data)
    try:
        send = requests.post(url, data=json_data, headers=headers)
        respons = send.json()
    except requests.exceptions.RequestException as e:
        respons = {
            "result": False,
            "Error": str(e),
            "description": None
        }
        return respons
    else:
        return respons

def get_http(url, params = None):
    try:
        response = requests.get(url, params)
    except requests.exceptions.RequestException as e:
        log_err(e)
        return False
    except Exception as a:
        log_err(a)
        return False
    else:
        data = response.json()
        return data


if __name__ == "__main__":
    data = {"zone-read": {"sendblock": {"cmd": "conf-read","section": "server"},"receive": {"type": "block"}}}
    response = get_http(urls)
    while True:
        if response:
            knots = send_http(urls_knot, data)
            if knots['result']:
                data = json.loads(knots['data']['data'])
                try:
                    data['status']
                except Exception:
                    pass
                else:
                    if data['status'] == False:
                        log_err("Knot Response: "+ str(data['status']))
                        error = data['error']
                        if error=='invalid parameter (data: None)':
                            log_err("Knot Status : Check Your Knot")
                        exit()
                log_rep("Agen Execute : "+knots['status'])
                log_rep("Knot Response: "+ str(True))
                log_rep("Synronizing: "+ response['status'])
                log_rep("Messages: "+ response['message'])
                exit()
            exit()
        else:
            response = get_http(urls)