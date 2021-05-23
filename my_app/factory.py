from flask import Flask
from .helpers import register_blueprints


def create_app(package_name, package_path, settings_override=None,
               register_security_blueprint=False):
    """Returns a :class:`Flask` application instance configured with common
    functionality for the Overholt platform.
    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: a dictionary of settings to override
    :param register_security_blueprint: flag to specify if the Flask-Security
                                        Blueprint should be registered.
                                        Defaults to `True`.
    """
    app = Flask(package_name, instance_relative_config=True)

    app.config.from_object('my_app.settings')
    app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object(settings_override)

    register_blueprints(app, package_name, package_path)

    return app
