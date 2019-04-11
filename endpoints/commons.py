import json
import logging

MESSAGE_NO_ERROR = "N/A"
STATUS_SUCCESS = "SUCCESS"


def construct_response(status=STATUS_SUCCESS, message=MESSAGE_NO_ERROR):
    """
    Constructs a JSON response for endpoints with side-effects.
    """
    if message != MESSAGE_NO_ERROR:
        logging.log(logging.DEBUG, message)

    response = {
        "status": status,
        "messsage": message
    }

    return json.dumps(response)
