import os

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, relationship
import click
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from datetime import datetime
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from sqlalchemy import ForeignKey



migrate = Migrate()
jwt = JWTManager()



class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class Role(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates='role')
    

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(default=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"),nullable=True)
    role: Mapped["Role"] = relationship(back_populates='user')
        

    def __repr__(self):
        return f"User( id={self.id!r}, username={self.username!r} )"

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]= mapped_column(nullable=False)
    body: Mapped[str]= mapped_column(nullable=False)
    created:Mapped[datetime] = mapped_column(server_default=sa.func.now())
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def __repr__(self):
        return f"Post( id={self.id!r}, title={self.title!r}, authorId={self.author_id!r} )"


@click.command('init-db')
def init_db_command():
    with current_app.app_context():
        db.create_all()
    click.echo('Initialized the database.')



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI="sqlite:///blog.sqlite",
        JWT_SECRET_KEY='super-secret',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    app.cli.add_command(init_db_command)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from src.controllers import user
    from src.controllers import auth
    from src.controllers import role
    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)

    return app