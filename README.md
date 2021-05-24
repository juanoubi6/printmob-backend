#Printmob-backend
Backend de la aplicacion Printmob

#Levantar proyecto localmente en Pycharm (recomendado)
1. Pararse en el directorio raiz
1. Levantar la base de datos con `docker-compose up db`
1. Correr las migraciones con `alembic upgrade head`
1. Correr el main del archivo wsgi.py

#Crear una nueva migracion
1. Correr `alembic revision -m "Descripcion de la migracion"`. Se va a crear un archivo en el directorio /alembic/versions
1. Modificar el archivo agregando la migracion (tanto el upgrade como el downgrade)
1. Ejecutar la migracione utilizando `alembic upgrade head`
