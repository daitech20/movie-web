PYTHON=poetry run python

runserver:
	${PYTHON} manage.py runserver 0.0.0.0:8001

migrate:
	${PYTHON} manage.py migrate

migrations:
	${PYTHON} manage.py makemigrations

collectstatic:
	${PYTHON} manage.py collectstatic --noinput

createsuperuser:
	${PYTHON} manage.py createsuperuser

worker:
	${PYTHON} -m celery -A movie_web worker -l info

beat:
	${PYTHON} -m celery -A movie_web beat

run_dev:
	make migrations
	make migrate
	make runserver

docker-up-redis:
	docker compose --env-file envs/.env up -d redis

docker-down-redis:
	docker compose --env-file envs/.env down redis

docker-up-postgres:
	docker compose --env-file envs/.env up -d postgres

docker-down-postgres:
	docker compose --env-file envs/.env down postgres

docker-build:
	make docker-down
	docker compose --env-file envs/.env build django
	docker compose --env-file envs/.env up -d django

docker-up:
	docker compose --env-file envs/.env up -d django

docker-down:
	docker compose --env-file envs/.env down django
