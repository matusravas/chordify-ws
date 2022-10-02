from functools import wraps
from flask import request


SECRET_KEY = "QpYKUpLjvFXUJ2zZD4l62Pg3iRyKbFcA"
TOKEN = "2lpbxtDLNIO4yKgIQOjaJxw8qBzSkbvh"


def authorize(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        ok = check_auth_token()
        return fn(*args, **kwargs) if ok else ('Missing Authorization header', 401)
    return wrapper


def check_auth_token():
    request_token = request.headers.get('Authorization', None)
    return True if request_token == TOKEN else False