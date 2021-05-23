from my_app.api import create_app
from flask.cli import FlaskGroup


class DevConfig(object):
    DEBUG = True


def create_test_app():
    return create_app(settings_override=DevConfig)


cli = FlaskGroup(create_app=create_test_app)

if __name__ == '__main__':
    cli()
