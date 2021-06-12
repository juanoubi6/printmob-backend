build: 
	docker-compose build --no-cache

run:
	docker-compose up -d

stop:
	docker-compose down

test:
	echo "Esto requiere que hayas hecho make run"
	docker exec -it printmob-backend_backend_1 python3 -m pytest tests/

migrate:
	docker exec -ti printmob-backend_backend_1 alembic upgrade head

push:
	aws ecr get-login-password --region us-east-2 --profile printmob | docker login --username AWS --password-stdin 715052550658.dkr.ecr.us-east-2.amazonaws.com
	docker tag printmob-backend_backend:latest 715052550658.dkr.ecr.us-east-2.amazonaws.com/printmob-backend:latest
	docker push 715052550658.dkr.ecr.us-east-2.amazonaws.com/printmob-backend:latest
