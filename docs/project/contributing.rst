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

  $ cockroach start --insecure --host=localhost

RESTKNOT API
^^^^^^^^^^^^

Clone the project `<https://github.com/BiznetGIO/RESTKnot/>`_

Go to the API directory

.. code-block:: bash

  $ cd api/


RESTKnot API consume the configuration from OS environment variables. So make
sure you have set them. Take a look into `.env.example` and change the default
values according to your situation.

Then run the app:

.. code-block:: bash

  $ flask run


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
      image: wurstmeister/kafka
      ports:
          - "9092:9092"
      environment:
          KAFKA_ADVERTISED_HOST_NAME: localhost
          KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181


RESTKNOT Agent
^^^^^^^^^^^^^^

Go to the Agent directory

.. code-block:: bash

  $ cd agent/

Set appropriate configurations. Take a look at `.env.example` in agent directory
and run them manually. At this moment RESTKNOT Agent doesn't load them automatically.

You can run the Agent in user mode, but some OS need superuser in order for knot
to create DNS records. `-E` argument is used to supply regular user OS
environment to sudo user.

.. code-block:: bash

  $ sudo -E ~/.virtualenvs/rest-knot/bin/dnsagent start master
