
IMG_NAME ?= chainlit

build:
	cd deployment && docker build -t ${IMG_NAME} .

run:
	cd deployment && docker compose up -d

log:
	cd deployment && docker compose logs -f

ps:
	cd deployment && docker compose -f docker-compose.yaml ps 

down:
	cd deployment && docker compose down

cook:
	cd deployment && docker compose down -v --remove-orphans

restart: down run

check:
	cd deployment && docker compose exec chainlit printenv