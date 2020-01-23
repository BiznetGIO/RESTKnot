#!/bin/bash

# setup cockroach
sudo apt-get install -y wget
wget -qO- https://binaries.cockroachdb.com/cockroach-v19.2.2.linux-amd64.tgz | tar  xvz
sudo cp -i cockroach-v19.2.2.linux-amd64/cockroach /usr/local/bin/

# start cockroach
cockroach start --insecure --host=localhost --background
cockroach sql --insecure --host=localhost --execute="CREATE DATABASE knotdb"
cockroach sql --insecure --host=localhost --database=knotdb < api/schema.sql

pip install -r api/requirements.txt
pip install -r api/requirements-dev.txt
pytest -vv -s api/tests/integration/
