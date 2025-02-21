IMG_NAME ?= ollama-extended

build:
	cd deployment && docker build -t $(IMG_NAME) .
run:
	cd deployment && docker compose up -d

down:
	cd deployment && docker compose down

cook:
	cd deployment && docker compose down -v --remove-orphans

restart: down run

ps:
	cd deployment && docker compose ps --no-trunc

logs:
	cd deployment && docker compose logs -f

help:
	@echo "build - build the docker image (default: ollama-extended, override with IMG_NAME=<name>)"
	@echo "run - run the docker container"
	@echo "down - stop the docker container"
	@echo "cook - stop the docker container and remove volumes"
	@echo "restart - restart the docker container"
	@echo "ps - list the docker containers"
	@echo "logs - show the logs of the docker container"
	@echo "help - show this help message"