from typing import Dict
from functools import wraps
from flask import request
from app import AUTH_TOKEN

def sort_fun_tabs(e: Dict):
    if 'votes' in e and 'rating' in e:
        return e['votes'] * e['rating']
    else:  
        return -1


def sort_fun_hits(e: Dict):
    if 'hits' in e:
        return int(e['hits'])
    else:  
        return -1


def authorize(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        ok = check_auth_token()
        return fn(*args, **kwargs) if ok else ('Missing Authorization header', 401)
    return wrapper


def check_auth_token():
    request_token = request.headers.get('Authorization', None)
    return True if request_token == AUTH_TOKEN else False