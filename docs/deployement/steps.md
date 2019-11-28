# Deployment Steps

## Build docker images

```
$ docker build -f Dockerfile -t restknot-api:0.7.0 .
$ docker build -f Dockerfile -t restknot-agent:0.7.0 .
```

## Export image to tar

```
$ docker save restknot-agent:0.7.0 > restknot-agent-0.7.0.tar
$ docker save restknot-api:0.7.0 > restknot-api-0.7.0.tar
```

Update the playbook value to corresponds you tar locations.

## Prepare the initial database

We've use bootstrap script to initialize database on remote machine, but it's
error prone and hard to maintain. so we come up with this simpler way

```
# start the cockroach instance
$ cockroach start --insecure --host=localhost

# create the db
$ cockroach sql --insecure
> create database knotdb;

# create the table
$ cockroach sql --insecure --database=knotdb < schema.sql
```

Update the playbook value to corresponds you initial database locations.

# Prepare application configs

You need `servers.yml` and `knot.conf`.

servers.yml contains of server and slave configuration for knot clustering, see
[servers.yml example](examples/servers.yml) example, and knot.conf serve as a
config for you knot app, see [knot.conf example](examples/knot.conf)


## Prepare the docker-compose fill

Replace the example value with the real one in the docker-compose.yml

## Get the keys of you machines

- Put the key of your machine in one directory .e.g `~/vm-keys/`
- Point the ansible to those keys .e.g

```
[api]
10.10.10.10 ansible_user=centos ansible_private_key_file="~/ssh-keys/vm-key.pem"

[knot-master]
11.11.11.11 ansible_user=centos ansible_private_key_file="~/ssh-keys/vm-key.pem"

[knot-slave]
12.12.12.12 ansible_user=centos ansible_private_key_file="~/ssh-keys/vm-key.pem"
```

## Play the Playbook

```
$ ansible-playbook initial-setups.yml -f 10 -v
$ ansible-playbook deploy-images-api.yml -f 10 -v
$ ansible-playbook deploy-images-agent.yml -f 10 -v

# to stop the container
$ ansible-playbook stop-containers.yml -f 10 -v
```
