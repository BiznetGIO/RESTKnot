from .parse import parser
from .utility import utils

def read_rest(data):
    try:
        data = parser.initialiaze(data)
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
            # "description": initialiaze_command,
            "status": "Command Execute",
            "data": data
        }
        return response
    