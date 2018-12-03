# REST KNOT
Easier way to manage your Knot

## Pre
RESTKnot consists of 2 different applications, namely: API and AGENT

## Features


# Before You Begin

## AGENT
Agent is a link between KNOT and API to make the API accessible for users.

### Environment File
An environment file is needed to run the Agent, create new environment file and save it as .env or rename .env.example by  typing following command to your terminal.

```
mv .env.example .env
```
#### Environment file's content
```
#------------------------------------------------------#
#                APP CONFIG                            #
#------------------------------------------------------#
APP_NAME = RESTKnot
APP_HOST = 127.0.0.1
APP_PORT = 6967
APP_VERSION = 0.0.1
APP_RELEASE = 0.0.1
APP_CREATED = BIZNETGIO
SECRET_KEY = secret

FLASK_DEBUG = True

#------------------------------------------------------#
#                KNOT CONFIG                           #
#------------------------------------------------------#

KNOT_SOCKET = /var/run/knot/knot.sock


#------------------------------------------------------#
#                REDIS CONFIG                          #
#------------------------------------------------------#
FLASK_REDIS_URL = redis://:pass@host:6379/0


JWT_SECRET_KEY = secret
```

## Prequisites
To run Agent in your server you need to install Knot DNS first since Agent needs Knot DNS to operate. 

For information about KNOT installation go to the following [link](https://gitlab.labs.nic.cz/knot/knot-dns/blob/master/README)


At the time neo-api only support Python3 or newer.

``` bash
pip3 install -r requirements.txt
```

After Installing Requirement File, Next Install redis

Fedora Based
``` bash
dnf install redis redis-cli
```

Debian based
``` bash
apt-get install redis redis-cli
```

### Run Knot DNS 

From your terminal type the following command

``` bash
sudo systemctl start knot
```
### Running Agent Server
Open second terminal and set your environment to Agent

``` bash
sudo env/bin/python manage.py server
```

Set Your Redis auth accourding to your .env file by typing the following command to your terminal

``` bash
redis-cli
127.0.0.1:6379> CONFIG SET requirepass "password"

```

### Start Cockroach DB Local Cluster (Insecure)

Type the following command to your terminal
``` bash
cockroach start --insecure --listen-addr=localhost
```
For further information of cockroachdb's command and installation go to [action](https://www.cockroachlabs.com/docs/stable/install-cockroachdb-linux.html)


### Runing Server
After local cluster is running, you can start the Agent's server using
``` bash
sudo python manage.py server
```


Installing InfluxDB Reference [action](https://docs.influxdata.com/influxdb/v1.7/introduction/installation/)



## Dockerize Development


# API Development
Serves to manage your KNOT server
## Installing

## Environment File
Create New Environment File save to .env or move .env.example 
```
mv .env.example .env
```
Value Environment File
```
#------------------------------------------------------#
#                APP CONFIG                            #
#------------------------------------------------------#
APP_NAME = RESTKnot
APP_HOST = 127.0.0.1
APP_PORT = 6968
APP_VERSION = 0.0.1
APP_RELEASE = XXX
APP_CREATED = BIZNETGIO

#------------------------------------------------------#
#                REDIS CONFIG                          #
#------------------------------------------------------#
FLASK_DEBUG = True
FLASK_REDIS_URL = redis://:pass@127.0.0.1:6379/0

#------------------------------------------------------#
#                CELERY CONFIG                         #
#------------------------------------------------------#
CELERY_BROKER_URL = redis://:pass@127.0.0.1:6379/1
CELERY_RESULT_BACKEND = redis://:pass@127.0.0.1:6379/1

#------------------------------------------------------#
#             INFLUXDB CONFIG                          #
#------------------------------------------------------#

INFLUXDB_HOST = localhost
INFLUXDB_PORT = 8086
INFLUXDB_USER = knot
INFLUXDB_PASSWORD = knot123
INFLUXDB_DATABASE = knotdb

#------------------------------------------------------#
#               SOCKET CONFIG                          #
#------------------------------------------------------#
SOCKET_AGENT_HOST = 127.0.0.1
SOCKET_AGENT_PORT = 6967

```




## Dockerize Development