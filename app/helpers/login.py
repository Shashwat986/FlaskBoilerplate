from functools import wraps
from flask import request


def check_user_logged_in(f):
    @wraps(f)
    def __decorated(*args, **kwargs):
        r = request.get_json()

        if "hello" not in r or r["hello"] != "world":
            return {"success": False, "message": "Password Error"}

        return f(*args, **kwargs)

    return __decorated
