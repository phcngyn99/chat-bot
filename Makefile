
IMG_NAME ?= chainlit
NETWORK_NAME ?= datacore
SUBNET ?= 172.16.0.0/16

build:
	cd deployment && docker build -t ${IMG_NAME} .

run:
	cd deployment && docker compose up -d

log:
	cd deployment && docker compose logs -f

ps:
	cd deployment && docker compose -f docker-compose.yaml ps --no-trunc

down:
	cd deployment && docker compose down

cook:
	cd deployment && docker compose down -v --remove-orphans

restart: down run

check:
	cd deployment && docker compose exec chainlit printenv

test: build cook run log

network:
	@echo "Creating network $(NETWORK_NAME) with subnet $(SUBNET)"
	@docker network create --subnet=$(SUBNET) $(NETWORK_NAME)

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build     Build the docker image"
	@echo "  run       Run the docker container"
	@echo "  log       Show the logs of the container"
	@echo "  ps        Show the status of the container"
	@echo "  down      Stop the container"
	@echo "  cook      Stop the container and remove volumes"
	@echo "  restart   Restart the container"
	@echo "  check     Check the environment variables"
	@echo "  test      Build, cook, run, and log the container"
	@echo "  help      Show this help message"
	@echo ""
	@echo "Variables:"
	@echo "  IMG_NAME  The name of the docker image (default: chainlit)"
	@echo ""
	@echo "Examples:"
	@echo "  make build"
	@echo "  make build IMG_NAME=chainlit"
	@echo "  make run"
	@echo "  make log"
	@echo "  make ps"
	@echo "  make down"
	@echo "  make cook"
	@echo "  make restart"
	@echo "  make check"
	@echo "  make test"
