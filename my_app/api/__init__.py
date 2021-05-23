from functools import wraps

from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

from . import builder
from .controllers import TestController
from .. import factory
from ..helpers import JSONEncoder
from .config import db_config


def create_app(env, settings_override=None, register_security_blueprint=False):
    """Returns the Overholt API application instance"""

    app = factory.create_app(
        __name__, __path__, settings_override,
        register_security_blueprint=register_security_blueprint)

    # Set the default JSON encoder
    app.json_encoder = JSONEncoder

    # Inject db
    db = create_db(app, env)

    # Inject controllers
    builder.inject_controllers(app, db)

    return app


def create_db(app, env):
    database_config = db_config[env]
    app.config['SQLALCHEMY_DATABASE_URI'] = database_config['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = database_config['SQLALCHEMY_TRACK_MODIFICATIONS']
    db = SQLAlchemy(app)
    app.db = db

    return db


def route(bp, *args, **kwargs):
    kwargs.setdefault('strict_slashes', False)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            status_code = 200
            response_value = f(*args, **kwargs)
            if isinstance(response_value, tuple):
                status_code = response_value[1]
                response_value = response_value[0]
            return jsonify(response_value), status_code

        return f

    return decorator
