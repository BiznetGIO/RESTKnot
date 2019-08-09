.PHONY: default isvirtualenv

SERVER_ENV ?= development

default:
	@echo "Local examples:"
	@echo "    make isvirtualenv     # Check wether virtualenv is active or not"
	@echo "    make server           # Start the server"
	@echo "    make setenv           # Set environment file"
	@echo "    make test             # Run test"

	@echo "    ENV PRODUCTION
	@echo "    make build            # Build the container"
	@echo "    make up               # Build and run the container"
	@echo "    make start            # Start containers"
	@echo "    make stop             # Stop running containers"
	@echo "    make rm               # Stop and remove running containers"

	@echo "    ENV DEVELOPMENT
	@echo "    make devel            # Build the container"
	@echo "    make updevel          # Build and run the container"
	@echo "    make startdevel       # Start containers"
	@echo "    make stopdevel        # Stop running containers"
	@echo "    make rmdevel          # Stop and remove running containers"

	@echo "    make celery           # Make Celery Setup"
	@echo "    make flower           # Make Flower Setup"

# Set environment file
setenv:
	cp environments/$(SERVER_ENV)/.env.example .env

# Check  wether virtualenv is active or not
isvirtualenv:
	@if [ -z "$(VIRTUAL_ENV)" ]; then echo "ERROR: Not in a virtualenv." 1>&2; exit 1; fi

# Run local server
server:
	python manage.py server

# Run Test
test:
	pytest --cov=app --cov-report=term-missing -vv

# DOCKER TASKS

# DEVEL
# Build the container
devel: ## Build the release and develoment container. The development
	docker-compose build

# Build and run the container
updevel: ## Spin up the project
	docker-compose up --build

startdevel:stopdevel ## Start containers
	docker-compose start

stopdevel: ## Stop running containers
	docker-compose stop

rmdevel: stop ## Stop and remove running containers
	docker-compose rm

# PRODUCTION
build:
	docker build -f Dockerfile.prod -t biznetgio/neo-openstack:prod .

up:
	docker-compose -f compose/docker-compose.yml up

start:stop
	docker-compose -f compose/docker-compose.yml start

stop:
	docker-compose -f compose/docker-compose.yml stop

rm: stop
	docker-compose -f compose/docker-compose.yml rm

# Celery
celery:
	docker-compose -f compose/docker-compose.yml.celery up

# Flower
flower:
	docker-compose -f compose/docker-compose.yml.flower up