# REST KNOT
Easier way to manage your Knot

## Pre
RESTKnot consists of 2 different applications, namely: API and AGENT

## Features


# Before You Begin
## Prequisites 
--------------------------

At the time neo-api only support Python3 or newer. Install the required module both on API and AGENT side. 

``` bash
pip3 install -r requirements.txt
```


## API 
To run AGENT in your server, you need to install the following prequisites first on the API side after installing requirements:



1.  [KnotDNS](https://www.knot-dns.cz/download/)
2.  [redis-cli](https://redis.io/download)
3.  [CockroachDB](https://www.cockroachlabs.com/docs/stable/install-cockroachdb-linux.html)


----------------------------

## Setting Up Environment

## AGENT

### Environment File
An environment file is needed to run the Agent, create new environment file and save it as .env or rename .env.example by  typing following command to your terminal.

```
mv .env.example .env
```
### [Environment file's content](https://raw.githubusercontent.com/BiznetGIO/RESTKnot/master/AGENT/.env.example)
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
SECRET_KEY = KNot6996KimciL

FLASK_DEBUG = True

#------------------------------------------------------#
#                KNOT CONFIG                           #
#------------------------------------------------------#

KNOT_SOCKET = /var/run/knot/knot.sock


#------------------------------------------------------#
#                REDIS CONFIG                          #
#------------------------------------------------------#
FLASK_REDIS_URL = redis://:pass@127.0.0.1:6379/0
KNOT_LIB = libknot.so.7

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


## Dockerize Development


## API Development
------------------------------
API serves to manage your KNOT server.
## Installing

## Prequisites
------------------------

### Environment File
Create New Environment File save to .env or move .env.example 
```
mv .env.example .env
```
### [Environment File's Content](https://raw.githubusercontent.com/BiznetGIO/RESTKnot/master/API/.env.example)

The following [content](https://raw.githubusercontent.com/BiznetGIO/RESTKnot/master/API/.env.example) is an example for API's local environment
```
### APP SETUP
APP_NAME = KNOT API
APP_HOST = 127.0.0.1
APP_PORT = 6968
SECRET_KEY = asdsagdasgdasf@asfdasgvdasda@#!@#!%$#%@#@@##
MEMCACHE_HOST=127.0.0.1
MEMCACHE_PORT=11211
FLASK_DEBUG = True

### REDIS SETUP
FLASK_REDIS_URL = redis://:pass@127.0.0.1:6379/0

### DATABASE SETUP
DB_NAME = knotdb
DB_HOST = localhost
DB_PORT = 26257
DB_USER = root
DB_SSL = disable

#### DOCS

SWAGGER_URL = '/api/docs'
SWAGGER_API_URL = 'http://127.0.0.1:6968/static/swagger.json'

### AGENT
SOCKET_AGENT_HOST = 'http://127.0.0.1'
SOCKET_AGENT_PORT = 6967

KNOT_LIB = libknot.so.7
```

Set Your Redis auth accourding to your .env file by typing the following command to your terminal

``` bash
redis-cli
127.0.0.1:6379> CONFIG SET requirepass "password"

```

### Configuring CockroachDB

### Start Cockroach DB Local Cluster (Insecure)

Type the following command to your terminal
``` bash
cockroach start --insecure --listen-addr=localhost
```
For further information of cockroachdb's command and installation go to [cockroach's page](https://www.cockroachlabs.com/docs/stable/install-cockroachdb-linux.html)


### Runing Server
After local cluster is running, you can start the Agent's server using
``` bash
sudo python manage.py server
```



## Dockerize Development