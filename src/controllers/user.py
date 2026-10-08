from flask import Blueprint, request
from ..app import User, db
from http import HTTPStatus
from sqlalchemy import inspect
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils import required_role

app = Blueprint('user', __name__, url_prefix='/users/')

def _create_user():
    data = request.json
    user = User(
        username=data["username"],
        password=data["password"],
        role_id=data["role_id"],
    )
    db.session.add(user)
    db.session.commit()


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            "id": user.id,
            "username": user.username,
            "role": {
                "role_id": user.role.id,
                "role_name": user.role.name
            }
        }for user in users
    ]

@app.route('', methods=["GET", "POST"])
@jwt_required()
@required_role("admin")
def list_or_create_users():
    if request.method == "POST":
        _create_user()
        return {"message": "User created"}, HTTPStatus.CREATED
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