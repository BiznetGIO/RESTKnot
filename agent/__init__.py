from agent.parser import parser
from agent.utility import utils

def read_rest(data):
    initialiaze_command = parser.initialiaze(data)
    try:
        parser.execute_command(initialiaze_command)
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
            "status": "Command Execute"
        }
        return response