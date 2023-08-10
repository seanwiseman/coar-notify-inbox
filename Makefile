.PHONY: install install-dev start start-services stop-services delete-db flake8 pylint lint

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

start: start-services
	uvicorn app:app --reload

start-services:
	docker compose up --detach

stop-services:
	docker compose down

delete-db: stop-services
	docker volume rm coar-notify-inbox_mongodb_data

flake8:
	flake8

pylint:
	pylint --fail-under=10 db routers tasks tests validation app.py config.py

lint: flake8 pylint