include .env

API_PORT ?= 8000

build:
	docker compose build

run:
	docker compose up -d

stop:
	docker compose down

remove:
	docker compose rm -f

clean-up: 
	docker compose down -v

start-up: run
