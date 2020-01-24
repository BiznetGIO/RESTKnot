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
  [
      {
        "zone_id": 512564293182357505,
        "zone": "example.com",
        "user": {
            "id": 512552858177372161,
            "email": "john@example.com"
        },
        "records": [
            {
                "id": 512564294432948225,
                "owner": "@",
                "rdata": "satu.mydns.id. hostmaster.mydns.id. 2019121601 10800 3600 604800 38400",
                "type": "SOA",
                "ttl": "3600"
            },
            {
                "id": 512564295907311617,
                "owner": "@",
                "rdata": "satu.mydns.id.",
                "type": "NS",
                "ttl": "3600"
            },
            {
                "id": 512564297375940609,
                "owner": "@",
                "rdata": "dua.mydns.id.",
                "type": "NS",
                "ttl": "3600"
            },
            {
                "id": 512564298888708097,
                "owner": "www",
                "rdata": "example.com.",
                "type": "CNAME",
                "ttl": "3600"
            }
        ]
    }
  ]

Get a domain by Zone
--------------------

.. code-block:: bash

  GET domain/list/zone/:zoneid

Response:

.. code-block:: bash


  Status: 200 OK
  ----
   {
        "zone_id": 512564293182357505,
        "zone": "example.com",
        "user": {
            "id": 512552858177372161,
            "email": "john@example.com"
        },
        "records": [
            {
                "id": 512564294432948225,
                "owner": "@",
                "rdata": "satu.mydns.id. hostmaster.mydns.id. 2019121601 10800 3600 604800 38400",
                "type": "SOA",
                "ttl": "3600"
            },
            {
                "id": 512564295907311617,
                "owner": "@",
                "rdata": "satu.mydns.id.",
                "type": "NS",
                "ttl": "3600"
            },
            {
                "id": 512564297375940609,
                "owner": "@",
                "rdata": "dua.mydns.id.",
                "type": "NS",
                "ttl": "3600"
            },
            {
                "id": 512564298888708097,
                "owner": "www",
                "rdata": "example.com.",
                "type": "CNAME",
                "ttl":  "3600"
            }
        ]
    }


Create domain
-------------

.. code-block:: bash

  POST /domain/add


Request body:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
user_id      int       The user id of the user
zone         string    The zone name
===========  =======   ===========================

Response:

.. code-block:: bash


  Status: 201 CREATED
  ----
   {
    "id": 512564293182357505,
    "zone": "example.com"
   }


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


  Status: 204 NO CONTENT
