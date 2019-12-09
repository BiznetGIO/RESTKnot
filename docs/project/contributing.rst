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
sure you have set them. Example:


.. code-block:: bash

  export FLASK_DEBUG=1
  export APP_HOST=0.0.0.0
  export APP_PORT=5000
  export DB_NAME=knotdb
  export DB_HOST=localhost
  export DB_PORT=26257
  export DB_USER=root
  export DB_SSL=disable
  export KAFKA_HOST=127.0.01
  export KAFKA_PORT=9092
  export DEFAULT_NS='satu.examplens.id. dua.examplens.id.'
  export DEFAULT_SOA_RDATA='satu.examplens.id. hostmaster.examplens.id. 10800 3600 604800 38400'
  export RESTKNOT_CLUSTER_FILE=/home/user/.config/restknot/servers.yaml
  export RESTKNOT_API_KEY=123


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

Set appropriate configurations. Example:

.. code-block:: bash

  export RESTKNOT_KNOT_LIB=/usr/lib/x86_64-linux-gnu/libknot.so
  export RESTKNOT_KNOT_SOCKET=/run/knot/knot.sock
  export RESTKNOT_KAFKA_BROKER=localhost
  export RESTKNOT_KAFKA_PORTS=9092
  export RESTKNOT_KAFKA_TOPIC=domaindata
  export RESTKNOT_KAFKA_FLAGS=master
  export RESTKNOT_KAFKA_GROUP=cmgz_master

You can run the Agent in user mode, but some OS need superuser in order for knot
to create DNS records.

.. code-block:: bash

  $ sudo -E ~/.virtualenvs/rest-knot/bin/dnsagent start master
