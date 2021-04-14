Contributing
############

General Contribution
--------------------

For general rule regarding contribution to BiznetGio projects. See `BiznetGio
Contributing Guide <https://biznetgio.github.io/guide/contrib-guide/>`_

Running the project locally
---------------------------

Cockroachdb
^^^^^^^^^^^

Install and run `cockroach DB <https://cockroachlabs.com/>`_

.. code-block:: bash

  $ cockroach start --insecure --listen-addr=localhost:26257 --http-addr=localhost:8090

It will store the log and data in the current directory. Otherwise, you need to use
``--store=foo`` to change the default. ``--http-addr`` is used for HTTP requests from the Admin UI. You can choose any
port you want if the default is already in use.


RESTKnot API
^^^^^^^^^^^^

Clone the project `<https://github.com/BiznetGIO/RESTKnot/>`_

Go to the API directory

.. code-block:: bash

  $ cd api/

  # create the virtualenv, then install the dependencies
  $ pip install -r requirements.txt


RESTKnot API consumes the configuration from OS environment variables. So make
sure you have set them. Take a look into code:`.example.env` and change the default
values according to your situation.

Then run the app:

.. code-block:: bash

  $ flask run


Ensure the app is running by checking the ``/api/health`` endpoint.

Broker
^^^^^^

For RESTKnot API to communicate with REStKnot Agent, they need a
broker. We use `Kafka` for the broker.

It's easier to use dockerized `Kafka` and `zookeeper`. Use the snippet below then
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


Ideally, you can choose any Kafka-docker version. But we develop using
``2.12-2.4.0``.

RESTKnot Agent
^^^^^^^^^^^^^^

Go to the Agent directory

.. code-block:: bash

  $ cd agent/

  # create the virtualenv, then install the dependencies
  $ pip install -r requirements.txt

Set appropriate configurations. Take a look at :code:`.example.env` in the agent directory
and run them manually. At this moment RESTKNOT Agent doesn't load them automatically.

You can run the Agent in user mode, but some OS need a superuser for the knot
to create DNS records. `-E` argument is used to supply a regular user OS
environment to sudo user.

.. code-block:: bash

  $ sudo -E ~/.virtualenvs/rest-knot/bin/dnsagent start master

Running the project using Docker Compose
----------------------------------------

We have provided the images so you can run them easily with docker-compose.

Grab ``api/docker-compose.yml`` and ``agent/docker-compose.yml``. Put them in
a separate directory, such as ``knot-api`` and ``knot-agent``. Then run the
following command to start the container:

.. code-block:: bash

  # do the same thing with knot-agent
  $ cd knot-api
  $ docker-compose up -d

Always keep in mind that you can't use :code:`localhost` or :code:`127.0.0.1` in
:code:`KAFKA_ADVERTISED_HOST_NAME` otherwise it won't work.

Basic Workflow
--------------

To test that all component works together, or to get an insight into how knot
works. See :ref:`howto:Basic Workflow`
