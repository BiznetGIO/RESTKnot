#!/bin/bash

redis-cli config set requirepass 'pass'
mv environtment/travis/env.example .env
mv environtment/travis/.coveragerc.example .coveragerc
mv environtment/travis/run_travis.sh run_travis.sh
mv environtment/travis/deploy.sh deploy.sh
