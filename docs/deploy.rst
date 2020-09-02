Deployment Steps
================

Prepare the initial database
----------------------------

We've used a bootstrap script to initialize the database on a remote machine, but it's
error-prone and hard to maintain. So we come up with this simpler way.

.. code-block:: bash

  # start the cockroach instance
  $ cockroach start --insecure --listen-addr=localhost:26257 --http-addr=localhost:8090

  # create the db
  $ cockroach sql --insecure
  > create database knotdb;

  # create the table
  $ cockroach sql --insecure --database=knotdb < schema.sql

Create the initial database on your local side, then update the corresponding
playbook tasks to match your initial database locations.

Prepare application configs
---------------------------

You need :code:`servers.yml` and :code:`knot.conf`.

:code:`servers.yml` contains a list of your masters and slaves name, and
:code:`knot.conf` serve as a configuration for your knot app. See more in
examples `directory <https://github.com/BiznetGIO/RESTKnot/tree/master/docs/deploy/examples>`_.

Prepare the docker-compose
--------------------------

Replace the example value with the real one in the docker-compose.yml
Most important things you have to pay attention to:

- `RESTKNOT_KAFKA_BROKER`
- `RESTKNOT_KNOT_LIB`
- `RESTKNOT_KNOT_SOCKET`
- `KAFKA_ADVERTISED_HOST_NAME`
- `RESTKNOT_API_KEY`

Get the keys of your machines
----------------------------

- Put the key of your machine in one directory .e.g `~/ssh-keys/`
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
  $ ansible-playbook setup-agent.yml -f 10 -v -e "server_type=master" -e "target_host=foo-master"
  # for slave servers
  $ ansible-playbook setup-agent.yml -f 10 -v -e "server_type=master" -e "target_host=bar-master"

  # to stop the container
  $ ansible-playbook stop-containers-api.yml -f 10 -v
  $ ansible-playbook stop-containers-agent.yml -f 10 -v -e "target_host=bar-master"

See more in playbook examples `directory <https://github.com/BiznetGIO/RESTKnot/tree/master/docs/deploy/playbooks>`_.
