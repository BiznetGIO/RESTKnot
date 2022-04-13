Contributing
############

General Contribution
--------------------

For general rule regarding contribution to BiznetGio projects. See `BiznetGio
Contributing Guide <https://biznetgio.github.io/guide/contrib-guide/>`_

Running the project locally
---------------------------

Below is the description of each step needed to run the project locally.
To try the command directly in order, see our playbook examples in ``docs/examples``.

Cockroachdb
^^^^^^^^^^^

It's recommended to use the CockroachDB docker image instead of installing it locally.

.. code-block:: yaml

    roach:
      hostname: roach
      image: cockroachdb/cockroach:v19.2.2
      command: start --insecure --listen-addr=roach:26257 --advertise-addr=roach:26257 --http-addr=roach:8090
      ports:
        - "26257:26257"
        - "8090:8090"
      volumes:
        - ./data/cockroach-data:/cockroach/cockroach-data:z

.. code-block:: console

  $ # run the cockroach container above
  $ docker-compose up -d
  $ # create database. `10.0.0.1` is your host IP.
  docker run --rm cockroachdb/cockroach:v19.2.2 sql --host=10.0.0.1:26257 --insecure --execute "CREATE DATABASE IF NOT EXISTS knotdb;"
  $ # create table. get the `schema.sql` in `api/`
  $ cat schema.sql | docker run -i --rm cockroachdb/cockroach:v19.2.2 sql --host=10.0.0.1:26257 --insecure --database=knotdb

This step will give you a running cockroach database, with ``knotdb`` as a name and a schema defined in ``schema.sql``.

RESTKnot API
^^^^^^^^^^^^

Clone the project `<https://github.com/BiznetGIO/RESTKnot/>`_

Go to the API directory

.. code-block:: bash

  $ cd api/

  # create the virtualenv, then install the dependencies
  $ pip install -r requirements.txt

After making changes, you can the ``restknot-api`` using plain ``flask run``.
Or running it via docker.

If you prefer to run without docker, you need to export the environment variables manually.
See ``api/docker-compose.example.yml`` to learn all available variables.

Using docker, it would be:

.. code-block:: console

  $ # build the image
  $ docker build -f Dockerfile -t restknot-api:0.7.8 --build-arg BUILD_VERSION=$(git log -1 --format=%h) .
  $ # run the image
  $ docker-compose up -d

Ensure the app is running by checking the ``/api/health`` endpoint.

Broker
^^^^^^

For RESTKnot API to communicate with RESTKnot Agent, they need a
broker. We use `Kafka` for the broker.

See ``docs/example`` to run Zookeeper and Kafka. The examples contain
configuration to run multiple Kafka with single Zookeeper or multiple Kafka with
multiple Zookeeper.

RESTKnot Agent
^^^^^^^^^^^^^^

To build the agent:

.. code-block:: console

  $ cd agent/

  $ # build the image
  $ docker build -f Dockerfile -t restknot-agent:0.7.8 --build-arg BUILD_VERSION=$(git log -1 --format=%h) .
  $ # run the image
  $ docker-compose up -d

Set appropriate configurations. Take a look at ``agent/docker-compose.example.yml``.

Basic Workflow
--------------

To test that all component works together, or to get an insight into how knot
works. See :ref:`howto:Basic Workflow`

Releasing
---------

To create a release. Run the following steps.

- Run linting ``./scripts/make is_verified``. To check if the codebase adheres to the rules.
- Update the CHANGELOG.
- Update version numbers using ``./scripts/bump_version <old-version> <new-version>``.
- Create a commit with a message format: `v[0-9]+.[0-9]+.[0-9]+`, and push it to a feature branch (as a pull request).
- Wait for a check to pass, merge the specified pull request to the master branch.
- Wait for a check to pass, create a release tag from GitHub UI, then copy the appropriate CHANGELOG to the release page.
