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

# function rabbit_mq(){
#     rep_warn "STARTING RABBITMQ"
#     docker pull rabbitmq:3-management
#     docker run -d -t -i -p 5672:5672 -e RABBITMQ_DEFAULT_USER="admin" -e RABBITMQ_DEFAULT_PASS="qazwsx" -e RABBITMQ_DEFAULT_VHOST="/" rabbitmq:3-management
#     rep_ok "STARTING RABBITMQ"
# }

function export_env(){
    export APP_HOST=localhost
    export APP_PORT=6969
    export APP_RELEASE=AMI
    export APP_CREATED=BIZNETGIO
    export FLASK_DEBUG=True
    export CELERY_BROKER_URL="amqp://admin:qazwsx@rabbitmq:5672//"
    export CELERY_RESULT_BACKEND="amqp://admin:qazwsx@rabbitmq:5672//"
    export DB_DRIVER=cockroach
    export DB_HOST=localhost
    export DB_PORT=26257
    export DB_NAME=biznet_home
    export DB_USER=root
    export DB_PASSWORD=
    export DB_SSL=disable

    export HB_APIKEY='eea675a4ca2b475dbc6a'
    export HB_API_ID='5edff06cbb0e9e75d49a'
    export HB_HOST_API='http://hostbill.biznetgio.net/admin/api.php'

    export TASK_PERIOD=900
    #export TASK_PERIOD=259200

    rep_ok "export $APP_HOST"
    rep_ok "export $APP_PORT"
    rep_ok "export $APP_RELEASE"
    rep_ok "export $APP_CREATED"
    rep_ok "export $FLASK_DEBUG"
    rep_ok "export $APP_REDIS_URL"
    rep_ok "export $CELERY_BROKER_URL"
    rep_ok "export $CELERY_RESULT_BACKEND"
}

if [[ -z $1 ]]; then
    concurent=2
    rep_warn "Using Default Concurent | $concurent"
fi

# rabbit_mq
export_env
celery worker -A celery_worker.celery --loglevel=info --concurrency=$concurent --beat
