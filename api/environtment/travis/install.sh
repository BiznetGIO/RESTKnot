#!/bin/bash
cd api
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
pip install coverage pytest pytest-cov pytest-ordering testfixtures
redis-cli config set requirepass 'pass'
mv environtment/travis/env.example .env
mv environtment/travis/.coveragerc.example .coveragerc
mv environtment/travis/run_travis.sh run_travis.sh
mv environtment/travis/deploy.sh deploy.sh

chmod +x run_travis.sh
./run_travis.sh


kill -9 `cat save_pid.txt`
rm save_pid.txt

cd ..