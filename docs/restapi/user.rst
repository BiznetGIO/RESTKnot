Users
=====

.. contents::
   :local:

Get all User
------------

.. code-block:: bash

  GET /user/list

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


Get a single user
-----------------

.. code-block:: bash

  GET /user/list/:id

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



Create user
-----------

.. code-block:: bash

  POST /user/add


Request body:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
email        string    The email of the user
project_id   string    The project id of the user
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



Edit user
---------

.. code-block:: bash

  PUT /user/edit/:id


Request body:

===========  =======   ===========================
Name         Type      Description
===========  =======   ===========================
email        string    The email of the user
project_id   string    The project id of the user
===========  =======   ===========================

Response:

.. code-block:: bash


  Status: 200 OK
  ----
   {
    "project_id": "001",
    "email": "john@example.com",
   }



Delete user
-----------

.. code-block:: bash

  DELETE /user/delete/:id


Response:

.. code-block:: bash


  Status: 200 OK