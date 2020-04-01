.. raw:: html

    <p align="center">
        <a href="#readme">
            <img alt="RESTKnot logo" src="https://github.com/BiznetGIO/RESTKnot/blob/master/docs/_static/img/resknot-banner.svg" height="150" width="500">
        </a>
    </p>

    <p align="center">
      <a href="https://restknot.readthedocs.io/en/latest/"><img alt="Documentation" src="https://img.shields.io/readthedocs/restknot.svg"></a>
      <a href="https://travis-ci.org/BiznetGIO/RESTKnot/"><img alt="Build status" src="https://img.shields.io/travis/BiznetGIO/RESTKnot.svg"></a>
      <a href="https://github.com/python/black"><img alt="Code Style" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
    </p>


========

Manage DNS records with asynchronous and simple APIs.

RESTKnot provide a high-level asynchronous API to existing Knot DNS server. This project consists of
three applications : RESTKnot agent, RESTKnot API, and RESTKnot CLI. A user can
create DNS record through web API provided by RESTKnot API, or as command line
app using RESTKnot CLI. Both of them send command to RESTKnot agent which will
be translated into Knot DNS action.

.. end-of-readme-intro

Features
--------

* Asynchronous operation
* Created default DNS records when adding new zone.
* Untangle all related record when deleting zone with single API.
* Prevent wrong RDATA format with validation support.
* Prevent record lost by checking RDATA contents before adding any record.

Take the tour
-------------

Create New Zone
^^^^^^^^^^^^^^^

.. code-block:: bash

  curl -X POST \
    http://localhost:5000/api/domain/add \
    -H 'X-API-key: 123' \
    -F user_id=001 \
    -F zone=example.com

Edit a Single Record
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

  curl -X PUT \
    http://127.0.0.1:5000/api/record/edit/10 \
    -H 'x-api-key: 123' \
    -F zone=bar.com \
    -F owner=@ \
    -F rtype=NS \
    -F rdata=one.exampledns.com. \
    -F ttl=3600

Delete a Zone
^^^^^^^^^^^^^

.. code-block:: bash

  curl -X DELETE \
    http://localhost:5000/api/domain/delete \
    -H 'X-API-Key: 123' \
    -F zone=example.com


Quick Start
-----------

To deploy the project, read the `deployment guide <https://restknot.readthedocs.io/en/stable/deploy.html>`_.
To run locally to make a contribution, read `how to run locally guide <https://restknot.readthedocs.io/en/stable/project/contributing.html#runing-the-project-locally>`_.

.. end-of-readme-usage

Project information
-------------------

* `Documentation <https://restknot.readthedocs.io/en/stable/index.html>`_
* `Contributing <https://restknot.readthedocs.io/en/stable/project/contributing.html>`_
* `Changelog <https://restknot.readthedocs.io/en/stable/project/changelog.html>`_
* `License <https://restknot.readthedocs.io/en/stable/project/license.html>`_
