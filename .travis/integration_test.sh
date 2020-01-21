#!/bin/bash


./test/integration/init_db.sh

cd api
virtualenv -p python3 env
source env/bin/activate

pip install -r requirements.txt
pip install -r requirements-dev.txt

pytest -vv -s tests/integration/
