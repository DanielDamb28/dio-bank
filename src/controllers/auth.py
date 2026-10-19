from flask import Blueprint, request
from ..models import User, db
from http import HTTPStatus
from sqlalchemy import inspect
from flask_jwt_extended import create_access_token
from src.app import bcrypt

app = Blueprint('auth', __name__, url_prefix='/auth')

def _senha_valida(hash, password):
    return bcrypt.check_password_hash(hash, password)

@app.route('/login/', methods=["POST"])
def login():
    username=request.json.get("username", None)
    password=request.json.get("password", None)
    user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()
    print(f"User: {user}")
    if not user or not _senha_valida(user.password, password):
        return {"msg": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(user.id))
    return {"access_token": access_token}, HTTPStatus.OK