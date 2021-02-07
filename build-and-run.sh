#!/usr/bin/env bash

set -ex

EXEC_CMD='docker-compose run backend'

docker-compose -f docker-compose.dev.yml up --build -d

${EXEC_CMD} python manage.py test