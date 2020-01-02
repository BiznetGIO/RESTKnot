How To’s
========

Create New Zone
---------------

To create new zone you first need to register using :code:`/user/add` then crate new
zone with :code:`/domain/add`. This will create SOA, NS, and CNAME record for you.


Add/Remove spesific Record
--------------------------

To add/ remove specific record you can use :code:`/record/add` and
:code:`record/delete/:record_id`


Remove zone completely
----------------------

To remove zone completely, which will remove all records. You can use :code:`/domain/delete`
