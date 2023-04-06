#Printmob-backend
Backend for Printmob app

#Before running
1. Create a .env file based on the .env.example file
1. In the .env file, input the values for the environment variables. These variables will be passed to your local container.

#Running the project with Docker
1. Navigate to the root directory
1. Run `make build` to create the containers
1. Run `make run` to create the database and the backend (which in turn runs the database migrations).

#Running the project locally in Pycharm
1. Navigate to the root directory
1. Run `make build` to create the containers
1. Run `make run`. This will start the database and the application, running the migrations.
1. Run `docker ps`, locate the backend container, and stop it with docker stop {containerId}.
1. Run the run method of the wsgi.py file locally. You can run it in debug mode for more control.

#Creating a new migration
1. Run `alembic revision -m "Description of the migration"`. This will create a file in the /alembic/versions directory.
1. Modify the file by adding the migration (both the upgrade and downgrade).
1. Run the migrations using `alembic upgrade head` (if you have it locally) or use `make migrate`.

#Pushing container to AWS cloud
1. Verify that there is an entry called printmob in the ~/.aws file.
1. Run `make push`.
1. Go to the AWS console or use the CLI to kill the running container so that the new container that is launched uses the new image.
