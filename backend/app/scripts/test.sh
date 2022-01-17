#!/usr/bin/env bash

set -e
set -x


pytest --capture=no --verbose app/tests/unit/ "${@}"
pytest --capture=no --verbose app/tests/integration/api_v2/ "${@}"
