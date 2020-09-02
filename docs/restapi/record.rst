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
        "id": 512565507407773697,
        "owner": "@",
        "rdata": "10 mail.example.com.",
        "zone": "example.com",
        "type": "MX",
        "ttl": "7200"
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
        "id": 512565507407773697,
        "owner": "@",
        "rdata": "10 mail.example.com.",
        "zone": "example.com",
        "type": "MX",
        "ttl":"ttl": "7200"
   }



Create record
-------------

.. warning::
   You can't have multiple records with the same content


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
ttl           int       The choice of preserved tll values
===========  =======   ===========================

Response:

.. code-block:: bash


  Status: 201 CREATED
  ----
   {
        "id": 512565507407773697,
        "owner": "@",
        "rdata": "10 mail.example.com.",
        "zone": "example.com",
        "type":  "MX",
        "ttl": "ttl": "7200"
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
ttl           int       The choice of preserved tll values
===========  =======   ===========================

Response:

.. code-block:: bash


  Status: 200 OK
  ----
  {
        "id": 512565507407773697,
        "owner": "@",
        "rdata": "10 mail.example.com.",
        "zone": "example.com",
        "type": "MX",
        "ttl": "7200"
   }



Delete record
-------------

.. code-block:: bash

  DELETE /record/delete/:id


Response:

.. code-block:: bash


  Status: 204 NO CONTENT
