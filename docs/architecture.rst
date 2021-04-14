Architecture
============

Code Base
---------

There are two top level component of RestKnot. First is ``resknot-api`` which
exposes the REST API to be consumed by the client. The app is built on top of
Flask. If you want to familiarize yourself with the codebase, the best way to start
is the controllers (``api/app/controllers``). ``domain.py`` acts as
an entry point after user registration (``user.py``). It serves the creation of
new zone and default records.

The second component is the ``agent``. It receives a JSON message from the
broker, parses it then sends a command to the Knot server via
``libknot.py``. It's a simple app and the main entry point is ``agent/dnsagent/clis/start.py``.


The Ecosystem
-------------

This part describes how ``resknot-api`` talks to ``resknot-agent`` and other
applications. You can also see the :ref:`deploy:Basic Deployment Architecture` to learn the basic form of RESTKnot
deployment.


.. figure:: /img/architecture.png
   :width: 400px
   :alt: RESTKnot Architecture

   A whole ecosystem.


To learn how each application talks with each other, let's start with a request
from the ``client``. Such as asking for new zone creation. The request is a REST API call
that is exposed by ``restknot-api``. While interacting with ``client``, it also
talks with ``database`` to store and retrieves new zones, user, etc. Then the
``restknot-api`` send a JSON message to ``message broker``.


.. figure:: /img/knot-master-slave.png
   :width: 250px
   :alt: Knot DNS master-slave

   Knot DNS master-slave

In turn, The ``broker`` pushes the message to all ``resknot-agent``
(including the slaves). The ``agent`` parses the message and send a command to
``Knot DNS server`` using ``libknot.py``

For creating a new zone. ``resknot-api`` will send 4 messages. The first message
contains  data to create zone config, it will be consumed by both ``master`` and
``slave`` agent.

.. raw:: html

   <details>
   <summary><a>first message</a></summary>

.. code-block:: json

     {
       "agent": {
         "agent_type": [
           "master",
           "slave"
         ]
       },
       "knot": [
         {
           "cmd": "conf-begin",
           "zone": "example.com"
         },
         {
           "cmd": "conf-set",
           "section": "zone",
           "item": "domain",
           "data": "example.com"
         },
         {
           "cmd": "conf-commit",
           "zone": "example.com"
         }
       ]
     }

.. raw:: html

   </details>


The second message contains data to create default records (SOA, NS,
CNAME). It's only consumed by ``master``.

.. raw:: html

   <details>
   <summary><a>second message</a></summary>

.. code-block:: json

     {
       "agent": {
         "agent_type": [
           "master"
         ]
       },
       "knot": [
         {
           "cmd": "zone-begin",
           "zone": "example.com"
         },
         {
           "cmd": "zone-set",
           "zone": null,
           "owner": "@",
           "rtype": "SOA",
           "ttl": "3600",
           "data": "one.dns.id. hostmaster.dns.id. 20 ..."
         },
         {
           "cmd": "zone-set",
           "zone": null,
           "owner": "@",
           "rtype": "NS",
           "ttl": "3600",
           "data": "one.dns.id."
         },
         {
           "//": "some messages omitted for brevity"
         },
         {
           "cmd": "zone-commit",
           "zone": "example.com"
         }
       ]
     }

.. raw:: html

   </details>


The third message contains data to set additional config such ``serial-policy``,
``notify``, and ``ACL``. The third and fourth message contains similar data,
only it's refined toward ``master`` agent or ``slave`` agent. This is why we
have to set ``RESTKNOT_AGENT_TYPE`` correctly. Otherwise, the zone can not be
created.

.. raw:: html

   <details>
   <summary><a>third message</a></summary>

.. code-block:: json

     [
       {
         "item": "notify",
         "data": "slave1",
         "cmd": "conf-set",
         "section": "zone",
         "zone": "example.com"
       },
       {
         "item": "notify",
         "data": "slave2",
         "cmd": "conf-set",
         "section": "zone",
         "zone": "example.com"
       },
       {
         "item": "acl",
         "data": "slave1",
         "cmd": "conf-set",
         "section": "zone",
         "zone": "example.com"
       },
       {
         "item": "acl",
         "data": "slave2",
         "cmd": "conf-set",
         "section": "zone",
         "zone": "example.com"
       }
     ]

.. raw:: html

   </details>


The fourth message contains similar data as the third, but it's only geared
toward ``slave``. Such ``notify`` keyword being changed to ``master``. These
keyword differences also represented in ``knot.conf`` and
``config.yml``. To learn more, take a look at ``knot.conf.master`` and
``knot.conf.slave`` in ``/deploy/examples/``.


.. raw:: html

   <details>
   <summary><a>fourth message</a></summary>

.. code-block:: json

    {
      "item":"master",
      "data":"master1",
      "cmd":"conf-set",
      "section":"zone",
      "zone":"example.com"
    }


.. raw:: html

   </details>

If we look closely at the figure above. Message broker pushing the message to all
``agent`` (represented by a straight line). In zone creation example, all the zone
config data is sent to all ``agent``. This is due to the fact that ``knot DNS
slaves`` can't create zone config automatically, so the ``agent`` there for it.

After the config is created in the ``slaves``. It starts talking with ``master`` via
``AXFR`` to receive zone's records and updates (represented by dotted line). But
before any zone's config is created, The ``slave`` can't do anything.

If config creation is done automatically in the ``slaves`` via ``AXFR`` maybe we
can get rid of the ``agent`` in the ``slaves`` entirely.
