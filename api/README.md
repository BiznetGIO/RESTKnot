[![Build Status](https://travis-ci.org/riszkymf/RESTKnot.svg?branch=testcase_travis)](https://travis-ci.org/riszkymf/RESTKnot)

# REST KNOT API

RESTKnot API is an API to manage DNS configuration on Knot Server. You can rest easy as RESTKnot will take care of your knot-dns configuration and manage your DNS the easy way.

## Prequisites
--------------------------------------
## Account
To access RESTKnot API, you have to create an account in [portal-neo](https://portal.neo.id/) first. 

------------------------------
## Requirements

- CockroachDB: Restknot uses CockroachDB as SQL Database. For information on CockroachDB's installation and command, you can go to their [page](https://www.cockroachlabs.com/docs/stable/install-cockroachdb-linux.html). Then you need to start CockroachDB. For information, click [here](https://www.cockroachlabs.com/docs/stable/start-a-local-cluster.html)

- Requirements file
    ``` bash
    pip3 install -r requirements.txt
    ```

- redis:  After Installing Requirement File, Next Install redis. Restknot use redis for cache. 

 
    Fedora Based
    ``` bash
    dnf install redis redis-cli
    ```

    Debian based
    ``` bash
    apt-get install redis redis-cli
    ```
------------------------
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
--------------------
## Further Reading
-  [Restknot API Documentation](docs/markdown/documentation)

- [Record Type and Its Content Rules](docs/markdown/documentation/RULES.md)

- [Rules on creating new domain](docs/markdown/documentation/RULES_add_domain.md)

- [Rules on creating new record](docs/markdown/documentation/RULES_add_record.md)


## Dockerize Development


## Documentation





