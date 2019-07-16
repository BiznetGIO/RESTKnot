from .parse import parser
from .utility import utils

def read_rest(data):
    initialiaze_command = parser.initialiaze(data)
    command_result = None
    try:
        command_result = initialiaze_command[0]['type']
    except Exception:
        command_result = None

    if command_result == "cluster" or command_result == "general":
        response={
            "result": True,
            "data": initialiaze_command,
            "status": "Command Execute",
            "description": data
        }
        return response
    try:
        data = parser.execute_command(initialiaze_command)
    except Exception as e:
        print("ERROR READ REST: ", e)
        response={
            "result": False,
            "error": str(e),
            "status": "Command Not Execute"
        }
        return response
    else:
        response={
            "result": True,
            "description": initialiaze_command,
            "status": "Command Execute",
            "data": data
        }
        return response
    