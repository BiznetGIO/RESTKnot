from flask import Response
import json

def response(status_code, message=None, data=None):
    """Response data helper

    Arguments:
        status_code {int} -- http status code

    Keyword Arguments:
        message {string} -- response message (default: {None})
        data {dict} -- data to be appended to response (default: {None})

    Returns:
        dict -- response data
    """
    success_status = {
        200: 'Operation succeeded',
        201: 'Created',
        202: 'Accepted',
        204: 'Reply does not contain additional content',
        304: 'Not modified'
    }

    failure_status = {
        400: 'Internal error occurred - unexpected error caused by request data',
        401: 'Unauthorized operation',
        403: 'Forbidden operation',
        404: 'Specified object not found',
        405: 'Method Not Allowed, for example, resource doesn\'t support DELETE method',
        406: 'Method Not Acceptable',
        409: 'Conflict',
        423: 'Locked',
        426: 'Upgrade Required',
        500: 'Internal Server Error - unexpected server-side error',
        501: 'Not Implemented - functionality is not implemented on the server side',
        503: 'Service is unavailable'
    }

    status = {}
    status['code'] = status_code

    if status_code in success_status:
        status['count'] = len(data) if data else 0
        status['data'] = data if data else None
        status['status'] = 'success'
        status['message'] = message if message else success_status[status_code]
    elif status_code in failure_status:
        status['status'] = 'error'
        status['message'] = message if message else failure_status[status_code]
    else:
        status['status'] = 'error'
        status['message'] = message if message else failure_status[400]

    response = Response(
            response=json.dumps(status),
            status=status_code, mimetype='application/json')

    return response
