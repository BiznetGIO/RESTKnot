from .parse import parser
from .utility import utils

def read_rest(data):
    try:
        initialiaze_command = parser.initialiaze(data)
        data = parser.execute_command(initialiaze_command)
    except Exception as e:
        response={
            "result": False,
            "error": str(e),
            "status": "Command Not Execute"
        }
        return response
    else:
        response={
            "result": True,
            "Description": initialiaze_command,
            "status": "Command Execute",
            "data": data
        }
        return response
    