#Printmob-backend
Backend de la aplicacion Printmob

#Antes de correr
1. Crear un archivo `.env` partiendo de `.env.example`
1. En él, colocar los valores de las variables de ambiente. Las mismas serán pasadas a tu container local

#Levantar proyecto con docker
1. Pararse en el directorio raiz
1. Ejecutar `make build` para crear los contenedores
1. Ejecutar `make run` para crear la base de datos y el backend (que a su vez corre las migraciones de la base de datos)

#Levantar proyecto localmente en Pycharm
1. Pararse en el directorio raiz
1. Correr `make build` para crear los contenedores
1. Correr `make run`. Esto levanta la base de datos y la aplicacion, corriendo las migraciones
1. Hacer `docker ps`, ubicar el container del backend y deterlo con `docker stop {containerId}`
1. Correr localmente el metodo run del archivo wsgi.py. Se puede correr debugeando para tener mas control

#Crear una nueva migracion
1. Correr `alembic revision -m "Descripcion de la migracion"`. Se va a crear un archivo en el directorio /alembic/versions
1. Modificar el archivo agregando la migracion (tanto el upgrade como el downgrade)
1. Ejecutar las migraciones utilizando `alembic upgrade head` (si lo tenemos local) o usar `make migrate`

#Pushear container a la nube de AWS
1. Verificar que haya una entrada llamada `printmob` en el archivo `~/.aws`
1. Correr `make push`
1. Ir a la consola de AWS o mediante la CLI, matar el container que esta corriendo para que el nuevo container que se lance use la nueva imagen
