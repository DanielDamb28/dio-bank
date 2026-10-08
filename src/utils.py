from flask_jwt_extended import get_jwt_identity
from src.app import User, db

from http import HTTPStatus
from functools import wraps


def required_role(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.get_or_404(User, user_id)
            if(not user or user.role.name != role_name):
                return {"message": "User don't have acess."}, HTTPStatus.FORBIDDEN
            return f()
        return wrapped
    return decorator


def eleva_quadrado(num):
    return num ** 2