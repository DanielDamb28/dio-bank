from src.app import ma
from marshmallow import fields
from src.views.role import RoleSchema

class UserSchema(ma.Schema):
    id = fields.Integer()
    username = fields.String()
    role = ma.Nested(RoleSchema)

class CreateUserSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    role_id = fields.Integer(required=True, strict=True)