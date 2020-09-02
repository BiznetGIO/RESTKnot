Contributing
############

General Contribution
--------------------

For general rule regarding contribution to BiznetGio projects. See `BiznetGio
Contributing Guide <https://biznetgio.github.io/guide/contrib-guide/>`_

Runing the project locally
--------------------------

Cockroachdb
^^^^^^^^^^^

Install and run `cockroachdb <https://cockroachlabs.com/>`_

.. code-block:: bash

  $ cockroach start --insecure --listen-addr=localhost:26257 --http-addr=localhost:8090

It will store the log and data in current directory. Otherwise, you need to use
``--store=foo`` to change the default. ``--http-addr`` is used for HTTP requests from the Admin UI. You can choose any
port you want if the default is already in use.


RESTKNOT API
^^^^^^^^^^^^

Clone the project `<https://github.com/BiznetGIO/RESTKnot/>`_

Go to the API directory

.. code-block:: bash

  $ cd api/

  # create the virtualenv, then install the depedencies
  $ pip install -r requirements.txt


RESTKnot API consume the configuration from OS environment variables. So make
sure you have set them. Take a look into :code:`.env.example` and change the default
values according to your situation.

Then run the app:

.. code-block:: bash

  $ flask run


Ensure the app is running by checking the ``/api/health`` endpoint.

Broker
^^^^^^

In order for RESTKnot API to communicate with REStKnot Agent, they need a
broker. We use `Kafka` for the broker.

It's easier to use dockerized `kafka` and `zookeper`. Use the snippet below then
run them using :code:`docker-compose -f docker-compose-kafka.yml up`

.. code-block:: yaml

  version: '3'
  services:
    zookeeper:
      image: wurstmeister/zookeeper
    kafka:
      image: wurstmeister/kafka:2.12-2.4.0
      ports:
          - "9092:9092"
      environment:
          KAFKA_ADVERTISED_HOST_NAME: localhost
          KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181


Ideally, you can choose any kafka-docker version. But we develop using
``2.12-2.4.0``.

RESTKNOT Agent
^^^^^^^^^^^^^^

Go to the Agent directory

.. code-block:: bash

  $ cd agent/

  # create the virtualenv, then install the depedencies
  $ pip install -r requirements.txt

Set appropriate configurations. Take a look at :code:`.env.example` in agent directory
and run them manually. At this moment RESTKNOT Agent doesn't load them automatically.

You can run the Agent in user mode, but some OS need superuser in order for knot
to create DNS records. `-E` argument is used to supply regular user OS
environment to sudo user.

.. code-block:: bash

  $ sudo -E ~/.virtualenvs/rest-knot/bin/dnsagent start master

Runing the project using Docker
-------------------------------

In order to run the project using docker. First you need to build both `api` and
`agent` image, then run them using docker compose. To see how to build them,
take a look at `Deployment Steps` section.

To run `api` (flask), `agent` (cli), and `broker` (kafka) container. You need to
provide the bridged network in their respective docker compose file. e.g:

.. code-block:: yaml

     kafka:
        image: wurstmeister/kafka
        ports:
            - '9092:9092'
        environment:
            KAFKA_ADVERTISED_HOST_NAME: 172.17.0.1
            KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
        networks:  # <--- add the network to kafka
            - agent_rknt-agent-net

   # put at the bottom of the file
   networks:
       agent_rknt-agent-net:
           external: true


Always keep in mind that you can't use :code:`localhost` or :code:`127.0.0.1` in
:code:`KAFKA_ADVERTISED_HOST_NAME` otherwise it won't work.

Basic Workflow
--------------

To test that all component works toghether, or to get an insight of how knot
works. See :ref:`howto:Basic Workflow`
