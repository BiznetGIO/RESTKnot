#!/bin/bash
sudo apt-get install systemd-services -y
sudo add-apt-repository ppa:cz.nic-labs/knot-dns -y
sudo apt-get update -y
sudo apt-get install knot -y
knotd -d -c knot.conf
docker login -u "$TEST_USER" -p "$TEST_PASS" registry.gitlab.com
echo RUN AGENT
cd agent
/usr/local/bin/docker-compose -f docker-compose.yml up -d
docker ps 
