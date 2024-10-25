run:
	docker-compose up -d --build

stop:
	docker-compose down

migrate:
	docker-compose exec web python manage.py migrate

tests:
	docker-compose exec web pytest

linter:
	docker-compose exec web flake8
