# REST KNOT API

RESTKnot API is an API to manage DNS configuration on Knot Server. You can rest easy as RESTKnot will take care of your knot-dns configuration and manage your DNS the easy way.

## Prequisites
### Account
To access RESTKnot API, you have to create an account in [portal-neo](https://portal.neo.id/) first. 

## Requirements

- CockroachDB: Restknot uses CockroachDB as SQL Database. For information on CockroachDB's installation and command, you can go to their [page](https://www.cockroachlabs.com/docs/stable/install-cockroachdb-linux.html). Then you need to start CockroachDB. For information, click [here](https://www.cockroachlabs.com/docs/stable/start-a-local-cluster.html)


- redis: Restknot use redis for cache. 

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

## Environment
Create New Environment File save to .env or move .env.example 
```
mv .env.example .env
```

See [example](environment/env.example) for further information on environment file.

## Runing Server
After local cluster is running, you can start the API server using
``` bash
python manage.py server
```
## Further Reading
- Restknot API Documentation [click](docs/markdown/documentation)


## Dockerize Development


