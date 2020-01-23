#!/bin/bash

# start db
psql -c 'create database knotdb;' -U postgres
psql knotdb < api/schema.sql

pip install -r api/requirements.txt
pip install -r api/requirements-dev.txt
pytest -vv -s api/tests/integration/
