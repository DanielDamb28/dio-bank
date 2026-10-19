import os

from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .models import db
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
ma = Marshmallow()


def create_app(enviroment=None):
    if enviroment is None:
        enviroment = os.getenv(
            'ENVIRONMENT',
            os.getenv('ENVIROMENT', 'development')
        )

    # create and configure the app
    app = Flask(
        __name__,
        instance_relative_config=True,
        root_path=os.path.dirname(os.path.abspath(__file__)),
        instance_path=os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'instance',
        ),
    )
    app.config.from_object(f'src.config.{enviroment.title()}Config')

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)

    from .controllers import user
    from .controllers import auth
    from .controllers import role
    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)

    return app