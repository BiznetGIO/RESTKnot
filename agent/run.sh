#!/bin/bash

command=$1
env=$2
worker=$3

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
    export APP_RELEASE=AMI
    export APP_CREATED=BIZNETGIO
    export WORKER=2
    export ENVIRONMENT=production
    export COMMAND=server

    rep_ok "export $APP_HOST"
    rep_ok "export $APP_PORT"
    rep_ok "export $APP_RELEASE"
    rep_ok "export $APP_CREATED"
}


function run_gunicorn(){
    apphost=$1
    port=$2
    worker=$3
    if [[ -z $1 ]]; then
        apphost=localhost
        rep_warn "Using Default Host $apphost"
    fi

    if [[ -z $2 ]]; then
        port=5000
        rep_warn "Using Default Port $port"
    fi

    if [[ -z $3 ]]; then
        worker=2
        rep_warn "Using Default Worker $worker"
    fi
    gunicorn production:app -b $apphost:$port -w $worker
}

if [ $command = 'server' ]
    then
    if [ $env = 'production' ]
        then
        rep_ok 'STARTING | SERVER'
        run_gunicorn $APP_HOST $APP_PORT $worker

    elif [ $env = 'development' ]
        then
        rep_warn "EXPORTING VARIABLE ENVIRONMENT"
        export_env
        rep_ok "EXPORTING VARIABLE ENVIRONMENT"
        echo ""
        rep_ok 'STARTING | SERVER'
        python3 manage.py server
    else
        rep_die '[env] : production | development'
    fi
else
    rep_die 'USAGE : ./run.sh server [env].'
fi

