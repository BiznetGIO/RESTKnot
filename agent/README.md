# AGENT
Agent works as DNS configurator on Knot Server. It took care of record and zone synchronization between database and knot server.

## Requirements

-  [KnotDNS](https://www.knot-dns.cz/download/)
- App requirements:
    ```
    pip install -r requirements.txt
    ```
---------------------------
## Environment File
An environment file is needed to run the Agent, create new environment file and save it as .env or rename .env.example by  typing following command to your terminal.

```
mv .env.example .env
```
**[Environment File Example](https://raw.githubusercontent.com/BiznetGIO/RESTKnot/master/AGENT/.env.example)**

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
-------------------------
## Setting Up Agent Server

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
----------------------------------
## Dockerize Development
```
docker build tag .
```
lingking your knot db, config and socket
then
set image tag in docker compose
```
docker-compose up
```

