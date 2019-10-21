#!/bin/bash


function rep_ok(){
    echo -e '\e[32m'$1'\e[m'
}

function rep_warn(){
    echo -e '\e[1;33mWARNING: '$1'\e[m'
}

function rep_die(){
    echo -e '\e[1;31mWARNING: '$1'\e[m'
    exit
}


function run_gunicorn(){
    apphost=$1
    port=$2
    worker=$3
    if [[ -z $1 ]]; then
        rep_warn "Using Default Host"
        apphost=localhost
    fi

    if [[ -z $2 ]]; then
        rep_warn "Using Default Port"
        port=5000
    fi

    if [[ -z $3 ]]; then
        rep_warn "Using Default Worker"
        worker=2
    fi
    gunicorn production:app -b $apphost:$port -w $worker
}

function export_env(){
    export APP_HOST=0.0.0.0
    export APP_PORT=5000
    export FLASK_DEBUG=True

    export KAFKA_HOST=127.0.01
    export KAFKA_PORT=9092

    export ACL='127.0.0.1/24, 10.10.3.0/24'

    export DEFAULT_NS='satu.neodns.id. dua.neodns.id.'
    export DEFAULT_SOA_CONTENT='satu.neodns.id. hostmaster.neodns.id.'
    export DEFAULT_SOA_SERIAL='10800 3600 604800 38400'

    rep_ok "export $APP_HOST"
    rep_ok "export $APP_PORT"
}



command=$COMMAND
env=$ENVIRONMENT
worker=$WORKER

if [[ -z $COMMAND ]]; then
    command=$1
    rep_warn "Using Default Host $command"
fi

if [[ -z $ENVIRONMENT ]]; then
    env=$2
    rep_warn "Using Default Host $env"
fi

if [ $command = 'server' ]
    then
    if [ $env = 'production' ]
        then
        rep_ok 'STARTING | SERVER'
        run_gunicorn $APP_HOST $APP_PORT $worker
    elif [ $env = 'staging' ]
        then
        rep_ok 'STARTING | SERVER STAGING'
        python3 manage.py server
    elif [ $env = 'development' ]
        then
        rep_ok "EXPORT ENV"
        export_env
        rep_ok 'STARTING | SERVER DEVELOPMENT'
        python3 manage.py server
    else
        rep_die '[env] : production | development'
    fi
else
    rep_die 'USAGE : ./run.sh server [env].'
fi
