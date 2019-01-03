# REST KNOT
Manage Your Knot Must Be Easy

## Pre
RESTKnot consists of 2 different applications, namely: API and AGENT

# AGENT
Is a link between KNOT and API so that the API can be accessed by users
## Environment File
Create New Environment File save to .env or move .env.local
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

## Installing
Install Agent at the same time as your KNOT server

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

Setup Your Redis auth see your .env file And Then

``` bash
redis-cli
127.0.0.1:6379> CONFIG SET requirepass "password"

```

Runing Server
``` bash
sudo python manage.py server
```


## Dockerize Development


# API Development
Serves to administer your KNOT server
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

DB_NAME = knotdb
DB_HOST = localhost
DB_PORT = 26257
DB_USER = root
DB_SSL = disable

#------------------------------------------------------#
#               SOCKET CONFIG                          #
#------------------------------------------------------#
SOCKET_AGENT_HOST = 127.0.0.1
SOCKET_AGENT_PORT = 6967

```

## Installing
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

Setup Your Redis auth see your .env file And Then

``` bash
redis-cli
127.0.0.1:6379> CONFIG SET requirepass "password"

```

Runing Server
``` bash
sudo python manage.py server
```

Installing CockroachDB Reference [action](https://www.cockroachlabs.com/docs/stable/)

## Dockerize Development