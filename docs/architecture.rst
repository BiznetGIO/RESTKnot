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

This part describes how each ``resknot-api`` talks to ``resknot-agent`` and other
applications. You can also see the :ref:`deploy:Basic Deployment Architecture` to learn the basic form of RESTKnot
deployment.


.. figure:: /img/architecture.png
   :width: 400px
   :alt: RESTKnot Architecture

   A whole ecosystem.


To learn how each application talks with each other, let's start with a request
from the ``client``. Such asking for new zone creation. The request is a REST API call
that is exposed by ``restknot-api``. While interacting with ``client``, it also
talks with ``database`` to store and retrieves new zones, user, etc. Then the
``restknot-api`` send a JSON message to ``message broker`` which in turns the
``broker`` pushes the message to all ``resknot-agent``. The ``agent`` parses the
message and send a command to ``knot server`` using ``libknot.py``


