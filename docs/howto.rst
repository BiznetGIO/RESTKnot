How To’s
========

Create New Zone
---------------

To create new zone you first need to register using :code:`/user/add` then crate new
zone with :code:`/domain/add`. This will create SOA, NS, and CNAME record for you.


Add/Edit/Remove spesific Record
-------------------------------

To add/edit/remove specific record you can use :code:`/record/add`,
:code:`/record/edit/:record_id`, and :code:`record/delete/:record_id`

.. note::
     RESTKnot handles SOA serial incremental automatically, so you don't need to
     hassle. But if the record you manage is SOA, you have to increment the serial
     manually.


Remove zone completely
----------------------

To remove zone completely, which will remove all records. You can use :code:`/domain/delete`
