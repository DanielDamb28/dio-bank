from flask import Blueprint, request
from ..models import User, db
from http import HTTPStatus
from sqlalchemy import inspect
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils import required_role
from src.app import bcrypt
from src.views.user import UserSchema, CreateUserSchema
from marshmallow import ValidationError

app = Blueprint('user', __name__, url_prefix='/users/')

def _create_user():
    schema = CreateUserSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    user = User(
        username=data["username"],
        password=bcrypt.generate_password_hash(data["password"]),
        role_id=data["role_id"],
    )
    db.session.add(user)
    db.session.commit()
    return {"message": "User created"}, HTTPStatus.CREATED


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    user_schema = UserSchema(many=True)
    return user_schema.dump(users)

@app.route('', methods=["GET", "POST"])
def list_or_create_users():
    if request.method == "POST":
        return _create_user()
    else:        
        return {"users": _list_users()}, HTTPStatus.OK

@app.route("<int:user_id>/")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
        "id": user.id,
        "username": user.username,
    }

@app.route("<int:user_id>/", methods=["PATCH", "PUT"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.get_json()
    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()
    return {
        "id": user.id,
        "username": user.username,
    }

@app.route("<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT