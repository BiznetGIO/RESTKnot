Knot Intro
==========

Knot is one of DNS server software that RESTKnot is built upon. RESTKnot uses
libknot python interface to talk with.

Installation
------------

.. code-block:: bash

  $ sudo apt-get install knot

Usage
-----

Every zone, which the knot server has to know about, must be specified in
two-part. First is the zone configuration which is saved in :code:`knot.conf`
and the zone data saved in the zone file.

An example of adding a new zone would be:

Add :code:`example.com` config into :code:`knot.conf`


.. code-block:: INI

   zone:
       - domain: example.com
         file: example.com.zone # zone data location


Then create a zone file that contains a zone data:


.. code-block:: INI

   $ORIGIN example.com.
   $TTL 3600
   example.com.  IN  SOA   one.dns.com. hostmaster.dns.com. 2020011301 3600 3600 604800 38400

Zone data format is standardized in  in RFC 1035 (section 5) and RFC 1034 (section 3.6.1). 

Start the Knot server (knotd) using :code:`systemctl start knot` or if it is
already running, you can reload the server using :code:`knotc reload`

.. code-block:: bash

    root@debian:/# knotc zone-read -- # no zone appears (expected)
    root@debian:/# knotc reload
    Reloaded

    root@debian:/# knotc conf-read  # default knot.conf
    server.rundir = /run/knot
    server.user = knot:knot
    server.listen = 127.0.0.1@53 ::1@53
    log.target = syslog
    log[syslog].any = info
    template.id = default
    template[default].storage = /var/lib/knot
    template[default].file = %s.zone
    zone.domain = example.com.
    zone[example.com.].file = example.com.zone

    root@debian:/# knotc zone-read --  # our zone created
    [example.com.] example.com. 3600 SOA one.dns.com. hostmaster.dns.com. 2020031100 3600 3600 604800 38400



Dynamic configuration
---------------------
.. warning::
     All changes made with the interactive tool (knotc) will be lost after the
     server stop if no binary database is created. With no binary database you also
     can't run :code:`conf-export`

Knot provides an interactive way to add a new zone using :code:`knotc`. :code:`knotc` is a user
front-end tool to control running server daemon (knotd). You need to initialize
or specify a binary database (confdb) to save all the changes you made. Otherwise,
all the changes to the configuration will be temporary (until the server is
stopped).

To add zone interactively, you need to create a binary database first. By
default this database located in :code:`/var/lib/knot/confdb` which consists of
two LMDB database :code:`data.mdb` and :code:`lock.mdb`. At the start, the default size of
:code:`confdb` directory is around 24K.

To create :code:`confdb` database, you can use :code:`conf-init` or :code:`conf-import`. For now
we use :code:`conf-import`.


.. code-block:: console

  $ sudo -u knot knotc conf-import /etc/knot/knot.conf # default conf

  $ sudo du -sh /var/lib/knot/confdb/ # check default size
    24K     confdb/

  $ # add the new zone using `conf-set` and `zone-set`
  $ knotc conf-begin; knotc conf-set 'zone[niu.com]'; knotc conf-commit
  # knotc zone-begin niu.com
  # knotc zone-set niu.com. 86400 SOA one.dns.id. hostmaster.dns.id. 2020011301 3600 3600 604800 38400
  # knotc zone-commit niu.com

  $ sudo knotc zone-read -- # new zone created interactively
    [niu.com.] niu.com. 86400 SOA one.dns.id. hostmaster.dns.id. 2020011301 3600 3600 604800 38400


At this point, we have created a new zone interactively. The next step is we have
to make sure our new zone config saved into :code:`confdb` and the zone data saved
into a corresponding zone file. Otherwise, it will be lost after we stop the knot
server.

.. code-block:: bash

    $ sudo du -sh confdb/ # size incremented
      32K     confdb/

    $ ls /var/lib/knot/ # check if zone file created
      confdb  niu.com.zone


If the size of :code:`confdb` incremented and a zone file created. Your newly created record will persist even after the knot server stopped or restarted.

Let's prove it.

.. code-block:: bash

    $ sudo systemctl stop knot
    $ sudo knotc zone-read -- # must be failed, because the knot server stopped
      error: failed to connect to socket '/run/knot/knot.sock' (not exists)

    $ systemctl start knot
    $ knotc zone-read -- # congratulations, you created a persistent zone using interactive way
      [niu.com.] niu.com. 86400 SOA one.dns.id. hostmaster.dns.id. 2020011301 3600 3600 604800 38400


DNS Querying
------------

We have created some zones. Let's query them.

.. code-block:: bash

    $ kdig @yourip niu.com SOA +short
      one.dns.id. hostmaster.dns.id. 2020011301 3600 3600 604800 38400


How Knot works
--------------

As explained previously that Knot saves zone data into two parts, zone
configuration, and zone data. At start, knot will load all the config from
:code:`knot.conf` and :code:`confdb` for zone configuration and zone files for zone data.

To check loaded zones, you can use :code:`knotc zone-read --` which will dump all the
zone data. To show loaded config run :code:`knotc conf-read`. :code:`--` denotes all zones,
you can tune this argument into more specific values.

Knot use three main part of storage in your machine:

- /etc/knot => to save the configuration :code:`knot.conf`
- /var/lib/knot => to save the zone files, binary database, journals, etc.
- /var/run/knot/ => to save the socket file

You can play with the files inside that storage to give a closer look into how Knot works.

.. code-block:: bash

    $ sudo systemctl stop knot # stop knot server
    $ mv mv niu.com.zone foo # remove zone file temporarily
    $ sudo systemctl start knot
    $ sudo knotc zone-read niu.com # no result (expected, after removing zone file)

    $ kdig @yourip niu.com SOA +short # this will return nothing

To restore the previous state. Stop the server, move the zone file, then
start the server again.


Importing Existing Zones
------------------------

Sometimes you need to move your existing zones to other machines manually (not
using AXFR/IXFR for some reason). These are steps that you need to take.

Prepare your old zone files that you can take from :code:`/var/lib/knot`, and export
your old zone configuration into a file using :code:`knotc conf-export`.

After preparing a new machine. Stop the running Knot server. Import the old
configuration. Move your old zone file to a new machine (either using scp or
rsycn), then start the server.

.. warning::
     This step will overwrite all the confdb content. There is no append
     mode. Make sure to export your new :code:`confdb` configurations if it is
     containing any record.

There is no append mode in importing a new configuration. So if you want to merge
two data from different sources, you can put them together manually in your
:code:`old.conf`.

.. code-block:: bash

    $ # in old machine
    $ sudo knotc conf-export /path/to/old.conf

    $ # in new machine
    $ sudo systemctl stop knot
    $ # import exiting config to the confdb
    $ sudo -u knot knotc -f -C /var/lib/knot/confdb/ conf-import /path/to/old.conf
    $ sudo du -sh confdb/ # check if import run well
      60K     confdb/

    $ # put your old zone file
    $ scp -r /home/user/old-zones/ remote@ip:/tmp/ # sometime you need to put to tmp first, because of permission
    $ cp /tmp/old-zones/* /var/lib/knot


    $ # make sure the owner is knot
    $ sudo chown -R knot /var/lib/knot
    $ sudo chgrp -R knot /var/lib/knot

    $ # start the server
    $ sudo systemctl start knot


Known Problems
--------------

- Knot can't load zone

  Make sure the zone file owner and group are :code:`knot`. And make sure the zone
  filename matches the zone configuration :code:`file` value.

- Knot can't create timers database

  Check the Knot storage owner, by default they must be:

  .. code-block:: bash

      - owner:group path
      - knot:knot /etc/knot/
      - knot:knot /var/lib/knot
      - knot:knot /var/lib/timers
      - knot:knot /var/run
      - knot:knot /var/run/knot.sock

  Make sure to execute :code:`knotc` that has a side effect (e.g database) with supplied
  :code:`knot` as the owner, e.g :code:`sudo -u knot conf-init`.

  For :code:`systemctl <cmd> knot` and :code:`knot` that has no side effect you can use normal :code:`root` user

- Knot refused to start

  Knot status stuck in ``activating``. Some of the errors of knot operation
  you will get would be: ``failed to connect to the socket (connection refused)`` or
  ``failed to open configuration database (operation not permitted)``.

  The workaround would be: 1) stop knot server 2) export existing zones using
  ``conf-export`` 3) remove ``confdb``, ``timers``, and ``journal`` directory 4) import using
  ``conf-import`` 5) start the server

  For more detailed information, read `Importing Existing Zones`_.

- RESTKnot Agent always exits after the start

  Producing ``KnotCtlError: connection reset (data: None)``.
  The workaround is to remove ``timers`` directory in ``/var/lib/knot``.
  Don't forget to make a backup. Then try to re-run the RESTKnot-agent.

  At first, the Agent will always exit. Producing ``ValueError: Can't connect to knot socket`` or ``KnotCtlError: connection reset``.
  This is expected. Currently, the Knot server has a socket issue, it can not handle a lot of requests in a second.
  So try to stop the Agent and start again. Usually, it takes two or three times, according to the amount of data that the Knot server loads.


Common Commands
---------------

These are common command operation to give you insight how to do things:

.. code-block:: console

    $ # start/stop the service
    # systemctl start knot
    # systemctl status knot
    # systemctl stop knot

    $ # create config
    # knotc conf-begin
    # knotc conf-set 'zone[niu.com]'
    # knotc conf-set 'zone[niu.com].file' 'niu.com.zone'
    # knotc conf-set 'zone[niu.com].notify' 'slave1 slave2'
    # knotc conf-set 'zone[niu.com].acl' 'slave1 slave2'
    # knotc conf-commit

    $ # create record
    # knotc zone-begin niu.com
    # knotc zone-set niu.com. @ 86400 SOA one.dns.id. hostmaster.dns.id. 2020011301 3600 3600 604800 38400
    $ # knotc zone-set <zone> <owner> <TTL> <rtype> <rdata>
    # knotc zone-set niu.com. ns1 86400 NS one.dns.id
    # knotc zone-set niu.com. @ 86400 CNAME niu.com.
    # knotc zone-set niu.com. @ 86400 A 2.2.2.2
    # knotc zone-set niu.com. @ 86400 MX mail.niu.com.
    # knotc zone-set niu.com. @ 86400 TXT "foobar"
    # knotc zone-commit niu.com

    $ # delete record
    # knotc zone-begin niu.com
    # knotc zone-unset niu.com ns1 # with specific owner
    # knotc zone-unset niu.com ns1 NS # with specific rrset
    # knotc zone-unset niu.com ns1 NS one.dns.id # with specific rdata
    # knotc zone-commit niu.com

    $ # see current config
    # knotc conf-read
    # knotc conf-read zone['niu.com']
    $ # or using grep
    # knotc conf-read | grep niu.com

    $ # check is record created
    # knotc zone-read --
    # knotc zone-read niu.com
    # knotc zone-read niu.com @ SOA
    $ # or using kdig/dig
    $ # use +tcp if your ISP provider annoys you
    $ kdig @localhost niu.com SOA +short +tcp

    $ # start everyting from scratch
    $ # stop knotd and knot-agent
    # rm -rf * /var/lib/knot # remove all knot db
    # rm -rf * /etc/knot # most of the time, it doesn't needed
    # sudo knotc conf-init # initialize the confdb
    $ # start knotd and knot-agent

    $ # export/backup the current state (config + records)
    # knotc conf-export /path/to/knot-backup.conf
    $ # import
    # knotc conf-import /path/to/knot-backup.conf
