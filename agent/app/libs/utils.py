import requests
import json

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