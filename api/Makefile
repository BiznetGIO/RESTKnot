.PHONY: default isvirtualenv docker

default:
	@echo "Local examples:"
	@echo "    make isvirtualenv     # Check wether virtualenv is active or not"
	@echo "    make run              # Start the server"
	@echo "    make rundocker        # Run docker from dockerfile"
	@echo "    make rundockercompose # Run docker from docker-compose.yml"

rundocker:
	docker build -t boilerplate:latest .
	docker run -d -p ${APP_PORT}:${APP_PORT} boilerplate

rundockercompose:
	docker-compose up

isvirtualenv:
	@if [ -z "$(VIRTUAL_ENV)" ]; then echo "ERROR: Not in a virtualenv." 1>&2; exit 1; fi

run:
	python manage.py server