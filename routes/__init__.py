import uuid
from functools import wraps

from flask import session, request, abort

from models.user import User

import redis
import json

cache1 = redis.StrictRedis()


def current_user():
    uid = session.get('user_id', '')
    u = User.one(id=uid)
    return u


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        v = cache1.get(str(u.id))
        t = json.loads(v)
        if token == t:
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    k = json.dumps(u.id)
    v = json.dumps(token)
    cache1.set(k, v)
    return token
