How To’s
========

Basic Workflow
--------------

First, you have to create a user by using the ``/user/add`` endpoint. Save returned
user ID then go to ``/domain/add`` to add new domains. It will create the default
records: 1) SOA, 2) NS, and 3) CNAME.

You can see you brand new domain info by going to
``/domain/list/zone/?name=example.com``. To get individual record info, use
``/record/list/:record_id``.

To make sure that the records were created on the Knot side. Use ``dig`` or ``kdig``:

.. code-block:: bash

  $ kdig @localhost example.com SOA +short


Add/Edit/Remove spesific Record
-------------------------------

To add/edit/remove specific record you can use :code:`/record/add`,
:code:`/record/edit/:record_id`, and :code:`record/delete/:record_id`

.. note::
     RESTKnot handles SOA serial incremental automatically, so you don't need to hassle. But if the record you manage is SOA, you have to increment the serial manually.


Remove zone completely
----------------------

To remove the zone completely, which will remove all records. You can use :code:`/domain/delete`
