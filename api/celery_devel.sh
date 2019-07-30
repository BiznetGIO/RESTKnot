#!/bin/bash

concurent=$1

function rep_ok(){
    echo -e '\e[32mSUCCESS | '$1'\e[m'
}
function rep_warn(){
    echo -e '\e[1;33mWARNING | '$1'\e[m'
}
function rep_die(){
    echo -e '\e[1;31mERROR | '$1'\e[m'
    exit
}

function export_env(){
    export APP_HOST=0.0.0.0
    export APP_PORT=6967
    export DB_NAME=knotdb
    # export DB_HOST=10.10.3.32
    export DB_HOST=localhost
    export DB_PORT=26257
    export DB_USER=root
    export DB_PASSWORD=
    export DB_SSL=disable
    # export SOCKET_AGENT_HOST=http://10.10.3.42
    export SOCKET_AGENT_HOST=http://127.0.0.1
    export SOCKET_AGENT_PORT=6967
    export ACL='127.0.0.1/24, 103.77.104.199/24, 10.150.24.11/24, 182.253.68.106/24, 180.249.0.28/24, 172.17.0.1/24'
    export FLASK_REDIS_URL=redis://:pass@session:6379/0
    export WORKER=2
    export ENVIRONMENT=production
    export COMMAND=server
    export DEFAULT_NS='satu.neodns.id. dua.neodns.id.'
    export DEFAULT_SOA_CONTENT='satu.neodns.id. hostmaster.neodns.id.'
    export DEFAULT_SOA_SERIAL='10800 3600 604800 38400'
    export CELERY_BROKER_URL="amqp://admin:qazwsx@172.17.0.1:5672//"
    export CELERY_RESULT_BACKEND="amqp://admin:qazwsx@172.17.0.1:5672//"
}

if [[ -z $1 ]]; then
    concurent=2
    rep_warn "Using Default Concurent | $concurent"
fi

export_env
celery worker -A celery_worker.celery --loglevel=info --concurrency=$concurent --beat