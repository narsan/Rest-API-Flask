from functools import wraps
from flask import request


def check_authority(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return {
                       "message": "Missing Token!",
                       "data": None,
                       "error": "Unauthorized"
                   }, 401

        else:
            return f(*args, **kwargs)

    return decorated