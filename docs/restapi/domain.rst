Domains
=======

.. contents::
   :local:

Get all Domain
--------------

.. code-block:: bash

  GET /domain/list

Response:

.. code-block:: bash


  Status: 200 OK
  ----

Get a domain by
---------------

.. code-block:: bash

  GET domain/list/zone/:zoneid
  GET domain/list/user/:projectid

Response:

.. code-block:: bash


  Status: 200 OK
  ----


Create domain
-------------

.. code-block:: bash

  POST /domain/add


Request body:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
project_id   string    The project id of the domain
zone         string    The zone name
===========  =======   ===========================

Response:

.. code-block:: bash


  Status: 200 OK


Delete domain
-------------

.. code-block:: bash

  DELETE /domain/delete/


Request body:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
zone         string    The zone name
===========  =======   ===========================

Response:

.. code-block:: bash


  Status: 200 OK
