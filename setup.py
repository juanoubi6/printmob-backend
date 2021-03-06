from distutils.core import setup

setup(
    name='Printmob',
    version='0.0.1',
    author='UTN-FRBA',
    license='LICENSE.txt',
    description='Printmob backend',
    long_description=open('README.md').read(),
    install_requires=[
        "flask==2.0.1",
        "gunicorn==19.10.0",
        "flask_sqlalchemy==2.5.0",
        "Flask-Migrate==3.0.0",
        "sqlalchemy==1.4.15",
        "psycopg2-binary==2.8.6",
        "pytest==6.2.4",
        "alembic==1.6.3",
        "jsonpickle==2.0.0",
        "flask-cors==3.0.10",
        "boto3==1.17.93",
        "schedule==1.1.0",
        "google-auth==1.32.1",
        "requests==2.25.1",
        "cachecontrol==0.12.6",
        "PyJWT==2.1.0",
        "mercadopago==2.0.7",
        "flask-compress==1.10.1"
    ],
)
