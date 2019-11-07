#!/bin/bash
echo Waiting for service to be up
sleep 10

host=roach-one

./cockroach sql --insecure --host="$host" --database=knotdb < /cockroach/schema.sql
