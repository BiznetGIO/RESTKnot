Records
=======

.. contents::
   :local:


Get all Record
--------------

.. code-block:: bash

  GET /record/list

Response:

.. code-block:: bash


  Status: 200 OK
  ----
  [
   {
    "id": "509436247274160129",
    "email": "john@example.com",
    "project_id": "001",
    "created_at": "2019-12-05 16:26:44.757773"
   }
  ]


Get a single record
-------------------

.. code-block:: bash

  GET /record/list/:id

Response:

.. code-block:: bash


  Status: 200 OK
  ----
   {
    "id": "509436247274160129",
    "email": "john@example.com",
    "project_id": "001",
    "created_at": "2019-12-05 16:26:44.757773"
   }



Create record
-------------

.. warning::
   You can't have multiple record with the exact same content


.. code-block:: bash

  POST /record/add


Request body:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
zone          string    The zone name
owner         string    The owner of the record
rtype         string    The record type
rdata         string    The record RDATA
ttl_id        string    The id of ttl
===========  =======   ===========================

Response:

.. code-block:: bash


  Status: 200 OK
  ----
   {
    "email": "john@example.com",
    "project_id": "001",
    "created_at": "2019-12-05 16:26:44.757773"
   }



Edit record
-----------

.. note::
   It’s necessary to increase SOA serial if you make any change to the record
   that contains serial.


.. code-block:: bash

  PUT /record/edit/:id


Request body:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
zone          string    The zone name
owner         string    The owner of the record
rtype         string    The record type
rdata         string    The record RDATA
ttl_id        string    The id of ttl
===========  =======   ===========================

Response:

.. code-block:: bash


  Status: 200 OK
  ----
   {
    "project_id": "001",
    "email": "john@example.com",
   }



Delete record
-------------

.. code-block:: bash

  DELETE /record/delete/:id


Response:

.. code-block:: bash


  Status: 200 OK
