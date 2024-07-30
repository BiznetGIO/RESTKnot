#!/bin/bash

# Install knot and postgresql
sudo apt-get install -y knot knot-libs libknot-dev
sudo apt-get install -y postgresql

# Start db
psql -c 'create database knotdb;' -U postgres
psql knotdb <api/tests/test_schema.sql

# Start knot
sudo cp api/tests/functional/knot.conf /etc/knot/knot.conf
sudo cp api/tests/functional/servers.yml ~/.config/restknot/
sudo service knot restart

pip install -r api/requirements.txt
pip install -r api/requirements-dev.txt

# Run kafka & zoookeper
docker-compose -f api/tests/functional/compose-kafka.yml up -d

# Run knot agent
pip install -e agent/
export RESTKNOT_AGENT_TYPE=master
# change according to your libknot.so path
export RESTKNOT_KNOT_LIB=/usr/lib/x86_64-linux-gnu/libknot.so
export RESTKNOT_KNOT_SOCKET=/run/knot/knot.sock
export RESTKNOT_KAFKA_BROKER=localhost
export RESTKNOT_KAFKA_PORTS=9092
export RESTKNOT_KAFKA_TOPIC=domaindata
# change according to your installation path
# must use sudo to talk with knot socket
sudo -E ~/.virtualenvs/rest-knot/bin/dnsagent start

# Run the test
pytest -vv -s api/tests/functional/

# Check kntotc read output
sudo knotc zone-read 'company.com'
if sudo knotc zone-read 'company.com' | grep -q 'company.com.'; then
  echo "Functional Test Passed"
fi
