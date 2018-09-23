#!/bin/bash

worker=$4

if [ ! $worker ]
    then
    echo "Use Default Worker"
    gunicorn server:app -b 0.0.0.0:6969 -w 2
else
    gunicorn server:app -b 0.0.0.0:6969 -w $worker
fi

