#!/bin/bash

# start DB
# can't use cockroach DB even if we managed to install it manually, the
# resulting test always failed in Travis environment (can't connect to
# cockroach DB). So we use PostgreSQL with our original schema.sql ported
psql -c 'create database knotdb;' -U postgres
psql knotdb < api/tests/integration/test_schema.sql

pip install -r api/requirements.txt
pip install -r api/requirements-dev.txt
pytest -vv -s api/tests/integration/
