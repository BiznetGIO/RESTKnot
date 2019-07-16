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

if [[ -z $1 ]]; then
    concurent=2
    rep_warn "Using Default Concurent | $concurent"
fi

celery worker -A celery_worker.celery --loglevel=info --concurrency=$concurent --beat