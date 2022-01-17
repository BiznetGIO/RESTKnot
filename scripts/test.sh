#! /usr/bin/env sh

# Exit in case of error
set -e

DOMAIN=api \
INSTALL_DEV=true \
docker-compose \
-f docker-compose.yml \
config > docker-stack.yml

docker-compose -f docker-stack.yml build
docker-compose -f docker-stack.yml down --volumes --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker-compose -f docker-stack.yml up --detach
# -T : Disable pseudo-tty allocation.
docker-compose -f docker-stack.yml exec -T api bash /app/tests-start.sh "$@"
docker-compose -f docker-stack.yml down --volumes --remove-orphans
