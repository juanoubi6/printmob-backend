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