.PHONY: up down build logs restart migrate shell test

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

restart:
	docker compose restart

migrate:
	docker compose run --rm $(SERVICE) python manage.py migrate

shell:
	docker compose run --rm $(SERVICE) python manage.py shell

test:
	docker compose run --rm $(SERVICE) pytest

ps:
	docker compose ps

clean:
	docker compose down -v
