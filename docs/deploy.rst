Deployment Steps
================

Build docker images
-------------------

.. code-block:: bash

  $ docker build -f Dockerfile -t restknot-api:0.7.0 .
  $ docker build -f Dockerfile -t restknot-agent:0.7.0 .

Export image to tar
-------------------

.. code-block:: bash


  $ docker save restknot-agent:0.7.0 > restknot-agent-0.7.0.tar
  $ docker save restknot-api:0.7.0 > restknot-api-0.7.0.tar


Update the playbook value to corresponds you tar locations.

Prepare the initial database
----------------------------

We've use bootstrap script to initialize database on remote machine, but it's
error prone and hard to maintain. so we come up with this simpler way

.. code-block:: bash

  # start the cockroach instance
  $ cockroach start --insecure --host=localhost

  # create the db
  $ cockroach sql --insecure
  > create database knotdb;

  # create the table
  $ cockroach sql --insecure --database=knotdb < schema.sql


Update the playbook value to corresponds you initial database locations.

Prepare application configs
---------------------------

You need :code:`servers.yml` and :code:`knot.conf`.

:code:`servers.yml` contains list of your masters and slaves name, see
:download:`deploy/examples/servers.yaml` example, and :code:`knot.conf` serve as a
config for you knot app, see :download:`deploy/examples/knot.conf.master` for
master config and :download:`deploy/examples/knot.conf.slave` for slave config.

Prepare the docker-compose
--------------------------

Replace the example value with the real one in the docker-compose.yml
Most important things you have to pay attention to:

- `RESTKNOT_KAFKA_BROKER`
- `RESTKNOT_KNOT_LIB`
- `RESTKNOT_KNOT_SOCKET`
- `KAFKA_ADVERTISED_HOST_NAME`
- `RESTKNOT_API_KEY`

Get the keys of you machines
----------------------------

- Put the key of your machine in one directory .e.g `~/vm-keys/`
- Point the ansible to those keys .e.g

.. code-block:: yaml

  [api]
  10.10.10.10 ansible_user=centos ansible_private_key_file="~/ssh-keys/vm-key.pem"

  [knot-master]
  11.11.11.11 ansible_user=centos ansible_private_key_file="~/ssh-keys/vm-key.pem"

  [knot-slave]
  12.12.12.12 ansible_user=centos ansible_private_key_file="~/ssh-keys/vm-key.pem"


Play the Playbook
-----------------

.. code-block:: bash

  $ ansible-playbook initial-setups.yml -f 10 -v
  $ ansible-playbook setup-api.yml -f 10 -v
  # for master servers
  $ ansible-playbook setup-agent.yml -f 10 -v -e "server_type=master"
  # for slave servers
  $ ansible-playbook setup-agent.yml -f 10 -v -e "server_type=slave"

  # to stop the container
  $ ansible-playbook stop-containers-api.yml -f 10 -v
  $ ansible-playbook stop-containers-agent.yml -f 10 -v
