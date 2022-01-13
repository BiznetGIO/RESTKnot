import json
from datetime import date, datetime
from typing import Callable, Dict, List, Union

from flask import Response


def json_serial(obj: Callable) -> Union[datetime, date]:
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    raise TypeError(f"Type {type(obj)} not serializable")


def response(
    status_code: int, message: str = None, data: Union[Dict, List] = None
) -> Response:
    """Response data helper

    Arguments:
        status_code {int} -- http status code

    Keyword Arguments:
        message {string} -- response message (default: {None})
        data {dict} -- data to be appended to response (default: {None})

    Returns:
        dict -- response data
    """
    success_status: Dict[int, str] = {
        200: "OK",
        201: "Created",
        202: "Accepted",
        204: "No Content",
        304: "Not modified",
    }

    failure_status: Dict[int, str] = {
        400: "Internal error occurred - unexpected error caused by request data",
        401: "Unauthorized operation",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed, for example, resource doesn't support DELETE method",
        406: "Method Not Acceptable",
        409: "Conflict",
        422: "Unprocessable Entity",
        423: "Locked",
        426: "Upgrade Required",
        500: "Internal Server Error",
        501: "Not Implemented - functionality is not implemented on the server side",
        503: "Service is unavailable",
    }

    _response: Dict = {}
    _response["code"] = status_code

    if status_code in success_status:
        count = 0
        if isinstance(data, list):
            count = len(data)
        if isinstance(data, dict):
            count = 1

        _response["count"] = count
        _response["data"] = data if data else None
        _response["status"] = "success"
        _response["message"] = message if message else success_status[status_code]
    elif status_code in failure_status:
        _response["status"] = "error"
        _response["message"] = message if message else failure_status[status_code]
    else:
        _response["status"] = "error"
        _response["message"] = message if message else failure_status[400]

    response_result = Response(
        response=json.dumps(_response, default=json_serial),
        status=status_code,
        mimetype="application/json",
    )

    return response_result
