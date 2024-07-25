include .env

API_PORT ?= 8000

build:
	docker image build --build-arg API_PORT=${API_PORT} -t test .

run:
	docker run -d --env-file .env --name test_run -p ${API_PORT}:${API_PORT} test

stop:
	docker stop test_run

remove:
	docker remove test_run

clean-up: 
	docker stop test_run && docker remove test_run

start-up: run
	run
