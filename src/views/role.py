from src.app import ma
from marshmallow import fields

class RoleSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()