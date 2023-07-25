.PHONY: install start start-services stop-services delete-db

install:
	pip install -r requirements.txt

start: start-services
	uvicorn app:app --reload

start-services:
	docker compose up --detach

stop-services:
	docker compose down

delete-db: stop-services
	docker volume rm coar-notify-inbox_mongodb_data
