#!/bin/bash
cd api
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
pip install coverage pytest pytest-cov pytest-ordering testfixtures
