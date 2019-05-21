CREATE TABLE zn_zone (
	id_zone INT NOT NULL DEFAULT unique_rowid(),
	nm_zone STRING(200) NULL,
	state INT NULL DEFAULT 0:::INT,
	CONSTRAINT "primary" PRIMARY KEY (id_zone ASC),
	UNIQUE INDEX zone_zone_name_key (nm_zone ASC),
	FAMILY "primary" (id_zone, nm_zone, state)
);

CREATE TABLE cs_master (
	id_master INT NOT NULL DEFAULT unique_rowid(),
	nm_master STRING NULL,
	ip_master STRING NULL,
	port STRING NULL DEFAULT '53':::STRING,
	CONSTRAINT master_pk PRIMARY KEY (id_master ASC),
	UNIQUE INDEX cs_master_un (nm_master ASC),
	FAMILY "primary" (id_master, nm_master, ip_master, port)
);

CREATE TABLE cs_acl_master (
	id_acl_master INT NOT NULL DEFAULT unique_rowid(),
	id_zone INT NULL,
	id_master INT NULL,
	state INT NOT NULL DEFAULT 0:::INT,
	create_date TIMESTAMPTZ NOT NULL DEFAULT now():::TIMESTAMPTZ,
	nm_acl VARCHAR NULL,
	CONSTRAINT cs_acl_master_pk PRIMARY KEY (id_acl_master ASC),
	INDEX cs_acl_master_auto_index_cs_acl_master_zone_fk (id_zone ASC),
	INDEX cs_acl_master_auto_index_cs_acl_master_cs_master_fk (id_master ASC),
	FAMILY "primary" (id_acl_master, id_zone, id_master, state, create_date, nm_acl)
);

CREATE TABLE cs_acl_master_log (
	id_cs_acl_master_log INT NOT NULL DEFAULT unique_rowid(),
	id_acl_master INT NOT NULL,
	messages VARCHAR NULL,
	command_type VARCHAR NULL,
	log_date TIMESTAMPTZ NOT NULL DEFAULT now():::TIMESTAMPTZ,
	CONSTRAINT cs_acl_master_log_pk PRIMARY KEY (id_cs_acl_master_log ASC),
	INDEX cs_acl_master_log_auto_index_cs_acl_master_log_cs_acl_master_fk (id_acl_master ASC),
	FAMILY "primary" (id_cs_acl_master_log, id_acl_master, messages, command_type, log_date)
);

CREATE TABLE cs_slave (
	id_slave INT NOT NULL DEFAULT unique_rowid(),
	nm_slave STRING NULL,
	ip_slave STRING NULL,
	port STRING NULL DEFAULT '53':::STRING,
	CONSTRAINT "primary" PRIMARY KEY (id_slave ASC),
	UNIQUE INDEX cs_slave_un (nm_slave ASC),
	FAMILY "primary" (id_slave, nm_slave, ip_slave, port)
);

CREATE TABLE cs_acl_slave (
	id_acl_slave INT NOT NULL DEFAULT unique_rowid(),
	id_acl_master INT NULL,
	id_slave INT NULL,
	state INT NULL DEFAULT 0:::INT,
	create_date TIMESTAMPTZ NOT NULL DEFAULT now():::TIMESTAMPTZ,
	CONSTRAINT cs_acl_slave_pk PRIMARY KEY (id_acl_slave ASC),
	INDEX cs_acl_slave_auto_index_cs_acl_slave_cs_acl_master_fk (id_acl_master ASC),
	INDEX cs_acl_slave_auto_index_cs_acl_slave_cs_slave_fk (id_slave ASC),
	FAMILY "primary" (id_acl_slave, id_acl_master, id_slave, state, create_date)
);

CREATE TABLE cs_acl_slave_log (
	id_cs_slave_log INT NOT NULL DEFAULT unique_rowid(),
	id_acl_slave INT NOT NULL,
	command_type VARCHAR NULL,
	messages VARCHAR NULL,
	log_date TIMESTAMPTZ NOT NULL DEFAULT now():::TIMESTAMPTZ,
	CONSTRAINT "primary" PRIMARY KEY (id_cs_slave_log ASC),
	INDEX cs_acl_slave_log_auto_index_cs_acl_slave_fk (id_acl_slave ASC),
	FAMILY "primary" (id_cs_slave_log, id_acl_slave, command_type, messages, log_date)
);

CREATE TABLE cs_notify_master (
	id_notify_master INT NOT NULL DEFAULT unique_rowid(),
	id_zone INT NULL,
	id_master INT NULL,
	state INT NOT NULL DEFAULT 0:::INT,
	column1 TIMESTAMPTZ NOT NULL DEFAULT now():::TIMESTAMPTZ,
	CONSTRAINT cs_notify_pk PRIMARY KEY (id_notify_master ASC),
	INDEX cs_notify_auto_index_cs_notify_cs_master_fk (id_master ASC),
	INDEX cs_notify_auto_index_cs_notify_zone_fk (id_zone ASC),
	FAMILY "primary" (id_notify_master, id_zone, id_master, state, column1)
);

CREATE TABLE cs_notify_master_log (
	id_cs_master_log INT NOT NULL DEFAULT unique_rowid(),
	id_notify_master INT NOT NULL,
	messages VARCHAR NULL,
	command_type VARCHAR NULL,
	log_date TIMESTAMPTZ NOT NULL DEFAULT now():::TIMESTAMPTZ,
	CONSTRAINT cs_notify_master_log_pk PRIMARY KEY (id_cs_master_log ASC),
	INDEX cs_notify_master_log_auto_index_cs_notify_master_log_cs_notify_master_fk (id_notify_master ASC),
	FAMILY "primary" (id_cs_master_log, id_notify_master, messages, command_type, log_date)
);

CREATE TABLE cs_notify_slave (
	id_notify_slave INT NOT NULL DEFAULT unique_rowid(),
	id_notify_master INT NULL,
	id_slave INT NULL,
	state INT NOT NULL DEFAULT 0:::INT,
	create_date TIMESTAMPTZ NOT NULL DEFAULT now():::TIMESTAMPTZ,
	CONSTRAINT cs_notify_slave_pk PRIMARY KEY (id_notify_slave ASC),
	INDEX cs_notify_slave_auto_index_cs_notify_slave_cs_slave_fk (id_slave ASC),
	INDEX cs_notify_slave_auto_index_cs_notify_slave_cs_notify_master_fk (id_notify_master ASC),
	FAMILY "primary" (id_notify_slave, id_notify_master, id_slave, state, create_date)
);

CREATE TABLE cs_notify_slave_log (
	id_cs_notify_slave_log INT NOT NULL DEFAULT unique_rowid(),
	id_notify_slave INT NOT NULL,
	messages VARCHAR NULL,
	command_type VARCHAR NULL,
	log_date TIMESTAMPTZ NOT NULL DEFAULT now():::TIMESTAMPTZ,
	CONSTRAINT cs_notify_slave_log_pk PRIMARY KEY (id_cs_notify_slave_log ASC),
	INDEX cs_notify_slave_log_auto_index_cs_notify_slave_log_cs_notify_slave_fk (id_notify_slave ASC),
	FAMILY "primary" (id_cs_notify_slave_log, id_notify_slave, messages, command_type, log_date)
);

CREATE TABLE userdata (
	userdata_id INT NOT NULL DEFAULT unique_rowid(),
	user_id STRING NOT NULL,
	project_id STRING(100) NOT NULL,
	created_at TIMESTAMP NULL DEFAULT current_timestamp():::TIMESTAMP,
	CONSTRAINT "primary" PRIMARY KEY (userdata_id ASC),
	UNIQUE INDEX userdata_user_id_key (user_id ASC),
	FAMILY "primary" (userdata_id, user_id, project_id, created_at)
);

CREATE TABLE zn_type (
	id_type INT NOT NULL DEFAULT unique_rowid(),
	nm_type STRING(100) NULL,
	CONSTRAINT "primary" PRIMARY KEY (id_type ASC),
	UNIQUE INDEX zn_type_un (nm_type ASC),
	FAMILY "primary" (id_type, nm_type)
);

CREATE TABLE zn_record (
	id_record INT NOT NULL DEFAULT unique_rowid(),
	id_type INT NULL,
	id_zone INT NULL,
	date_record STRING(200) NULL,
	nm_record STRING(200) NULL,
	state INT NULL DEFAULT 0:::INT,
	CONSTRAINT "primary" PRIMARY KEY (id_record ASC),
	INDEX record_auto_index_fk_id_type_ref_type (id_type ASC),
	INDEX record_auto_index_fk_id_zone_ref_zone (id_zone ASC),
	FAMILY "primary" (id_record, id_type, id_zone, date_record, nm_record, state)
);

CREATE TABLE zn_content_serial (
	id_content_serial INT NOT NULL DEFAULT unique_rowid(),
	id_record INT NULL,
	nm_content_serial STRING NULL,
	CONSTRAINT zn_content_serial_pk PRIMARY KEY (id_content_serial ASC),
	INDEX zn_content_serial_auto_index_zn_content_serial_zn_record_fk (id_record ASC),
	FAMILY "primary" (id_content_serial, id_record, nm_content_serial)
);

CREATE VIEW v_content_serial (id_content_serial, id_zone, nm_zone, nm_record, id_record, nm_type, nm_content_serial) AS SELECT m1.id_content_serial, m3.id_zone, m3.nm_zone, m2.nm_record, m2.id_record, m4.nm_type, m1.nm_content_serial FROM knotdb.public.zn_content_serial AS m1 JOIN knotdb.public.zn_record AS m2 ON m1.id_record = m2.id_record JOIN knotdb.public.zn_zone AS m3 ON m2.id_zone = m3.id_zone JOIN knotdb.public.zn_type AS m4 ON m2.id_type = m4.id_type;

CREATE TABLE zn_ttl (
	id_ttl INT NOT NULL DEFAULT unique_rowid(),
	nm_ttl STRING(50) NULL,
	CONSTRAINT "primary" PRIMARY KEY (id_ttl ASC),
	UNIQUE INDEX zn_ttl_un (nm_ttl ASC),
	FAMILY "primary" (id_ttl, nm_ttl)
);

CREATE TABLE zn_ttldata (
	id_ttldata INT NOT NULL DEFAULT unique_rowid(),
	id_record INT NOT NULL,
	id_ttl INT NOT NULL,
	created_at TIMESTAMP NULL DEFAULT current_timestamp():::TIMESTAMP,
	CONSTRAINT "primary" PRIMARY KEY (id_ttldata ASC),
	INDEX ttldata_auto_index_fk_id_record_ref_record (id_record ASC),
	INDEX ttldata_auto_index_fk_id_ttl_ref_ttl (id_ttl ASC),
	FAMILY "primary" (id_ttldata, id_record, id_ttl, created_at)
);

CREATE TABLE zn_content (
	id_content INT NOT NULL DEFAULT unique_rowid(),
	id_ttldata INT NULL,
	nm_content STRING NULL,
	CONSTRAINT zn_content_pk PRIMARY KEY (id_content ASC),
	INDEX zn_content_auto_index_zn_content_zn_ttldata_fk (id_ttldata ASC),
	FAMILY "primary" (id_content, id_ttldata, nm_content)
);

CREATE VIEW v_contentdata (id_content, id_zone, nm_zone, id_record, nm_record, nm_type, nm_ttl, nm_content) AS SELECT m1.id_content, m5.id_zone, m5.nm_zone, m3.id_record, m3.nm_record, m6.nm_type, m4.nm_ttl, m1.nm_content FROM knotdb.public.zn_content AS m1 JOIN knotdb.public.zn_ttldata AS m2 ON m1.id_ttldata = m2.id_ttldata JOIN knotdb.public.zn_record AS m3 ON m2.id_record = m3.id_record JOIN knotdb.public.zn_ttl AS m4 ON m2.id_ttl = m4.id_ttl JOIN knotdb.public.zn_type AS m6 ON m3.id_type = m6.id_type JOIN knotdb.public.zn_zone AS m5 ON m3.id_zone = m5.id_zone;

CREATE VIEW v_cs_acl_master (id_acl_master, id_master, id_zone, nm_zone, ip_master, nm_master, port) AS SELECT m1.id_acl_master, m1.id_master, m1.id_zone, m2.nm_zone, m3.ip_master, m3.nm_master, m3.port FROM knotdb.public.cs_acl_master AS m1 JOIN knotdb.public.zn_zone AS m2 ON m1.id_zone = m2.id_zone JOIN knotdb.public.cs_master AS m3 ON m1.id_master = m3.id_master;

CREATE VIEW v_cs_acl_slave (id_acl_slave, id_acl_master, id_slave, state, id_zone, ip_slave, nm_slave, port_slave, ip_master, nm_master, port_master, nm_zone) AS SELECT m1.id_acl_slave, m1.id_acl_master, m1.id_slave, m1.state, m2.id_zone, m3.ip_slave, m3.nm_slave, m3.port AS port_slave, m4.ip_master, m4.nm_master, m4.port AS port_master, m5.nm_zone FROM knotdb.public.cs_acl_slave AS m1 JOIN knotdb.public.cs_acl_master AS m2 ON m1.id_acl_master = m2.id_acl_master JOIN knotdb.public.cs_slave AS m3 ON m1.id_slave = m3.id_slave JOIN knotdb.public.cs_master AS m4 ON m2.id_master = m4.id_master JOIN knotdb.public.zn_zone AS m5 ON m2.id_zone = m5.id_zone;

CREATE VIEW v_cs_notify_master (id_notify_master, id_master, id_zone, nm_zone, state, ip_master, nm_master, port) AS SELECT m1.id_notify_master, m1.id_master, m1.id_zone, m2.nm_zone, m2.state, m3.ip_master, m3.nm_master, m3.port FROM knotdb.public.cs_notify_master AS m1 JOIN knotdb.public.zn_zone AS m2 ON m1.id_zone = m2.id_zone JOIN knotdb.public.cs_master AS m3 ON m1.id_master = m3.id_master;

CREATE VIEW v_cs_notify_slave (id_notify_slave, id_notify_master, id_slave, ip_slave, nm_slave, slave_port, ip_master, nm_master, master_port, id_zone, nm_zone, state) AS SELECT m1.id_notify_slave, m1.id_notify_master, m1.id_slave, m3.ip_slave, m3.nm_slave, m3.port AS slave_port, m4.ip_master, m4.nm_master, m4.port AS master_port, m5.id_zone, m5.nm_zone, m5.state FROM knotdb.public.cs_notify_slave AS m1 JOIN knotdb.public.cs_notify_master AS m2 ON m1.id_notify_master = m2.id_notify_master JOIN knotdb.public.cs_slave AS m3 ON m1.id_slave = m3.id_slave JOIN knotdb.public.cs_master AS m4 ON m2.id_master = m4.id_master JOIN knotdb.public.zn_zone AS m5 ON m2.id_zone = m5.id_zone;

CREATE VIEW v_record (id_record, id_zone, nm_zone, nm_record, date_record, nm_type, state) AS SELECT m1.id_record, m2.id_zone, m2.nm_zone, m1.nm_record, m1.date_record, m3.nm_type, m1.state FROM knotdb.public.zn_record AS m1 JOIN knotdb.public.zn_zone AS m2 ON m1.id_zone = m2.id_zone JOIN knotdb.public.zn_type AS m3 ON m1.id_type = m3.id_type;

CREATE VIEW v_share_zone_record (id_acl_slave, id_acl_master, id_slave, id_record, id_type, state, id_zone, ip_slave, nm_slave, port_slave, ip_master, nm_master, port_master, nm_zone, nm_record, date_record, state_record, nm_type) AS SELECT m1.id_acl_slave, m1.id_acl_master, m1.id_slave, m6.id_record, m7.id_type, m1.state, m2.id_zone, m3.ip_slave, m3.nm_slave, m3.port AS port_slave, m4.ip_master, m4.nm_master, m4.port AS port_master, m5.nm_zone, m6.nm_record, m6.date_record, m6.state AS state_record, m7.nm_type FROM knotdb.public.cs_acl_slave AS m1 JOIN knotdb.public.cs_acl_master AS m2 ON m1.id_acl_master = m2.id_acl_master JOIN knotdb.public.cs_slave AS m3 ON m1.id_slave = m3.id_slave JOIN knotdb.public.cs_master AS m4 ON m2.id_master = m4.id_master JOIN knotdb.public.zn_zone AS m5 ON m2.id_zone = m5.id_zone JOIN knotdb.public.zn_record AS m6 ON m5.id_zone = m6.id_zone JOIN knotdb.public.zn_type AS m7 ON m6.id_type = m7.id_type;

CREATE VIEW v_ttldata (id_ttldata, id_ttl, id_record, id_zone, nm_zone, nm_record, nm_ttl, nm_type) AS SELECT m1.id_ttldata, m1.id_ttl, m2.id_record, m4.id_zone, m4.nm_zone, m2.nm_record, m3.nm_ttl, m5.nm_type FROM knotdb.public.zn_ttldata AS m1 JOIN knotdb.public.zn_record AS m2 ON m1.id_record = m2.id_record JOIN knotdb.public.zn_ttl AS m3 ON m1.id_ttl = m3.id_ttl JOIN knotdb.public.zn_zone AS m4 ON m2.id_zone = m4.id_zone JOIN knotdb.public.zn_type AS m5 ON m2.id_type = m5.id_type;

CREATE TABLE zn_user_zone (
	id_user_zone INT NOT NULL DEFAULT unique_rowid(),
	userdata_id INT NOT NULL,
	id_zone INT NOT NULL,
	CONSTRAINT "primary" PRIMARY KEY (id_user_zone ASC),
	UNIQUE INDEX zn_user_zone_id_zone_key (id_zone ASC),
	INDEX user_zone_auto_index_fk_userdata_id_ref (userdata_id ASC),
	INDEX user_zone_auto_index_fk_id_zone_ref_zone (id_zone ASC),
	FAMILY "primary" (id_user_zone, userdata_id, id_zone)
);

CREATE VIEW v_userzone (id_user_zone, userdata_id, id_zone, user_id, project_id, nm_zone, state) AS SELECT m1.id_user_zone, m2.userdata_id, m3.id_zone, m2.user_id, m2.project_id, m3.nm_zone, m3.state FROM knotdb.public.zn_user_zone AS m1 JOIN knotdb.public.userdata AS m2 ON m1.userdata_id = m2.userdata_id JOIN knotdb.public.zn_zone AS m3 ON m3.id_zone = m1.id_zone;

INSERT INTO zn_zone (id_zone, nm_zone, state) VALUES
	(440099714981298177, 'janda3.com', 1),
	(440585424342024193, 'janda4.com', 1),
	(440590527158648833, 'gadis1.com', 1),
	(440591958449225729, 'gadis2.com', 1);

INSERT INTO cs_master (id_master, nm_master, ip_master, port) VALUES
	(402152439124393985, 'master1', '103.58.102.42', '6967');

INSERT INTO cs_acl_master (id_acl_master, id_zone, id_master, state, create_date, nm_acl) VALUES
	(440100908355289089, 440099714981298177, 402152439124393985, 1, '2019-04-04 11:48:58.534875+00:00', 'slave_acl'),
	(440585633688780801, 440585424342024193, 402152439124393985, 1, '2019-04-06 04:54:24.96823+00:00', NULL),
	(440590651466448897, 440590527158648833, 402152439124393985, 1, '2019-04-06 05:19:56.27198+00:00', NULL),
	(440592087915921409, 440591958449225729, 402152439124393985, 1, '2019-04-06 05:27:14.635494+00:00', NULL);

INSERT INTO cs_acl_master_log (id_cs_acl_master_log, id_acl_master, messages, command_type, log_date) VALUES
	(440100955715731457, 440100908355289089, e'error: (missing value) zone[janda3.com].acl\n', 'Add: acl', '2019-04-04 11:49:12.988697+00:00'),
	(440103854163984385, 440100908355289089, e'error: (not exists) zone[janda3.com].acl = slave1\n', 'Add: acl', '2019-04-04 12:03:57.524687+00:00'),
	(440104132659511297, 440100908355289089, e'error: (not exists) zone[janda3.com].acl = slave1\n', 'Add: acl', '2019-04-04 12:05:22.515391+00:00'),
	(440104353790951425, 440100908355289089, e'error: (not exists) zone[janda3.com].acl = slave1\n', 'Add: acl', '2019-04-04 12:06:29.998787+00:00'),
	(440104393391210497, 440100908355289089, e'error: (not exists) zone[janda3.com].acl = slave1\n', 'Add: acl', '2019-04-04 12:06:42.083824+00:00'),
	(440104521898524673, 440100908355289089, e'OK\n', 'Add: acl', '2019-04-04 12:07:21.301331+00:00'),
	(440104562516983809, 440100908355289089, e'OK\n', 'Add: acl', '2019-04-04 12:07:33.697131+00:00'),
	(440104634654425089, 440100908355289089, e'OK\n', 'Add: acl', '2019-04-04 12:07:55.711995+00:00'),
	(440122361972228097, 440100908355289089, e'OK\n', 'Add: acl', '2019-04-04 13:38:05.659583+00:00'),
	(440586458210009089, 440585633688780801, e'OK\n', 'Add: acl', '2019-04-06 04:58:36.591206+00:00'),
	(440591155147964417, 440590651466448897, e'OK\n', 'Add: acl', '2019-04-06 05:22:29.983746+00:00'),
	(440592392958574593, 440592087915921409, e'OK\n', 'Add: acl', '2019-04-06 05:28:47.733719+00:00');

INSERT INTO cs_slave (id_slave, nm_slave, ip_slave, port) VALUES
	(402152759030939649, 'slave1', '112.78.183.110', '6967');

INSERT INTO cs_acl_slave (id_acl_slave, id_acl_master, id_slave, state, create_date) VALUES
	(440118506067525633, 440100908355289089, 402152759030939649, 1, '2019-04-04 13:18:28.92987+00:00'),
	(440585918327160833, 440585633688780801, 402152759030939649, 1, '2019-04-06 04:55:51.832322+00:00'),
	(440590886338428929, 440590651466448897, 402152759030939649, 1, '2019-04-06 05:21:07.949348+00:00'),
	(440592177283858433, 440592087915921409, 402152759030939649, 1, '2019-04-06 05:27:41.914921+00:00');

INSERT INTO cs_acl_slave_log (id_cs_slave_log, id_acl_slave, command_type, messages, log_date) VALUES
	(440118895035187201, 440118506067525633, 'add: acl', e'error: (invalid identifier) zone[janda3.com].acl = notify_from_master\n', '2019-04-04 13:20:27.634305+00:00'),
	(440581530390298625, 440118506067525633, 'add: acl', e'error: (not exists) zone[janda3.com].acl = notify_from_master\n', '2019-04-06 04:33:32.740298+00:00'),
	(440581894849822721, 440118506067525633, 'add: acl', e'error: (not exists) zone[janda3.com].acl = notify_from_master\n', '2019-04-06 04:35:23.965131+00:00'),
	(440582182733086721, 440118506067525633, 'add: acl', e'error: (not exists) zone[janda3.com].acl = notify_from_master\n', '2019-04-06 04:36:51.819618+00:00'),
	(440582852816928769, 440118506067525633, 'add: acl', e'error: (not exists) zone[janda3.com].acl = notify_from_master\n', '2019-04-06 04:40:16.313117+00:00'),
	(440583395173105665, 440118506067525633, 'add: acl', e'error: (not exists) zone[janda3.com].acl = notify_from_master\n', '2019-04-06 04:43:01.826886+00:00'),
	(440583633693048833, 440118506067525633, 'add: acl', e'error: (not exists) zone[janda3.com].acl = notify_from_master\n', '2019-04-06 04:44:14.617258+00:00'),
	(440584014428471297, 440118506067525633, 'add: acl', e'error: (not exists) zone[janda3.com].acl = notify_from_master\n', '2019-04-06 04:46:10.80864+00:00'),
	(440584477672570881, 440118506067525633, 'Add: acl', e'OK\n', '2019-04-06 04:48:32.179414+00:00'),
	(440584930472427521, 440118506067525633, 'Add: acl', e'OK\n', '2019-04-06 04:50:50.362971+00:00'),
	(440585078185295873, 440118506067525633, 'Add: acl', e'OK\n', '2019-04-06 04:51:35.441701+00:00'),
	(440585127753220097, 440118506067525633, 'Add: acl', e'OK\n', '2019-04-06 04:51:50.567942+00:00'),
	(440586491766276097, 440585918327160833, 'Add: acl', e'OK\n', '2019-04-06 04:58:46.832171+00:00'),
	(440591182674722817, 440590886338428929, 'Add: acl', e'OK\n', '2019-04-06 05:22:38.384205+00:00'),
	(440592414454972417, 440592177283858433, 'Add: acl', e'OK\n', '2019-04-06 05:28:54.293807+00:00');

INSERT INTO cs_notify_master (id_notify_master, id_zone, id_master, state, column1) VALUES
	(440104887179313153, 440099714981298177, 402152439124393985, 1, '2019-04-04 12:09:12.775989+00:00'),
	(440585976147804161, 440585424342024193, 402152439124393985, 1, '2019-04-06 04:56:09.477657+00:00'),
	(440590950498893825, 440590527158648833, 402152439124393985, 1, '2019-04-06 05:21:27.529102+00:00'),
	(440592223358320641, 440591958449225729, 402152439124393985, 1, '2019-04-06 05:27:55.975886+00:00');

INSERT INTO cs_notify_master_log (id_cs_master_log, id_notify_master, messages, command_type, log_date) VALUES
	(440105397677064193, 440104887179313153, e'error: (missing value) zone[janda3.com].notify\n', 'add: notify', '2019-04-04 12:11:48.567782+00:00'),
	(440105747654377473, 440104887179313153, e'error: (missing value) zone[janda3.com].notify\n', 'add: notify', '2019-04-04 12:13:35.372079+00:00'),
	(440106079176327169, 440104887179313153, e'error: (missing value) zone[janda3.com].notify\n', 'add: notify', '2019-04-04 12:15:16.545063+00:00'),
	(440106247045349377, 440104887179313153, e'error: (missing value) zone[janda3.com].notify\n', 'add: notify', '2019-04-04 12:16:07.774432+00:00'),
	(440106371099197441, 440104887179313153, e'OK\n', 'Add: notify', '2019-04-04 12:16:45.632598+00:00'),
	(440122206866210817, 440104887179313153, e'OK\n', 'Add: notify', '2019-04-04 13:37:18.325368+00:00'),
	(440586411601362945, 440585976147804161, e'OK\n', 'Add: notify', '2019-04-06 04:58:22.367406+00:00'),
	(440591108889673729, 440590950498893825, e'OK\n', 'Add: notify', '2019-04-06 05:22:15.86694+00:00'),
	(440592342631055361, 440592223358320641, e'OK\n', 'Add: notify', '2019-04-06 05:28:32.374931+00:00');

INSERT INTO cs_notify_slave (id_notify_slave, id_notify_master, id_slave, state, create_date) VALUES
	(440106344094760961, 440104887179313153, 402152759030939649, 1, '2019-04-04 12:16:37.392032+00:00'),
	(440586039310483457, 440585976147804161, 402152759030939649, 1, '2019-04-06 04:56:28.753439+00:00'),
	(440591010226143233, 440590950498893825, 402152759030939649, 1, '2019-04-06 05:21:45.7564+00:00'),
	(440592265151873025, 440592223358320641, 402152759030939649, 1, '2019-04-06 05:28:08.730267+00:00');

INSERT INTO cs_notify_slave_log (id_cs_notify_slave_log, id_notify_slave, messages, command_type, log_date) VALUES
	(440108559750889473, 440106344094760961, e'error: (invalid item) zone[janda3.com].master master1\n', 'add: notify', '2019-04-04 12:27:53.556604+00:00'),
	(440108807214825473, 440106344094760961, e'error: (invalid item) zone[janda3.com].master master1\n', 'add: notify', '2019-04-04 12:29:09.076601+00:00'),
	(440116049710350337, 440106344094760961, e'error: (invalid item) zone[janda3.com].master master1\n', 'add: notify', '2019-04-04 13:05:59.310788+00:00'),
	(440118103813619713, 440106344094760961, e'error: (invalid item) zone[janda3.com].master master1\n', 'add: notify', '2019-04-04 13:16:26.172889+00:00'),
	(440579976452276225, 440106344094760961, e'error: (invalid item) zone[janda3.com].master master1\n', 'add: notify', '2019-04-06 04:25:38.516508+00:00'),
	(440579997649928193, 440106344094760961, e'error: (invalid item) zone[janda3.com].master master1\n', 'add: notify', '2019-04-06 04:25:44.985108+00:00'),
	(440580386881536001, 440106344094760961, e'error: (invalid item) zone[janda3.com].master master1\n', 'add: notify', '2019-04-06 04:27:43.769199+00:00'),
	(440580584176189441, 440106344094760961, e'error: (invalid item) zone[janda3.com].master master1\n', 'add: notify', '2019-04-06 04:28:43.979217+00:00'),
	(440580968454029313, 440106344094760961, e'error: (invalid item) zone[janda3.com].master master1\n', 'add: notify', '2019-04-06 04:30:41.250892+00:00'),
	(440581101663846401, 440106344094760961, e'error: (invalid item) zone[janda3.com].master master1\n', 'add: notify', '2019-04-06 04:31:21.903427+00:00'),
	(440582203540832257, 440106344094760961, e'error: (invalid item) zone[janda3.com].master master1\n', 'add: notify', '2019-04-06 04:36:58.16957+00:00'),
	(440582816245514241, 440106344094760961, e'OK\n', 'Add: notify', '2019-04-06 04:40:05.152214+00:00'),
	(440584915178487809, 440106344094760961, e'OK\n', 'Add: notify', '2019-04-06 04:50:45.695862+00:00'),
	(440586435025534977, 440586039310483457, e'OK\n', 'Add: notify', '2019-04-06 04:58:29.516498+00:00'),
	(440591129814728705, 440591010226143233, e'OK\n', 'Add: notify', '2019-04-06 05:22:22.252212+00:00'),
	(440592371509624833, 440592265151873025, e'OK\n', 'Add: notify', '2019-04-06 05:28:41.187908+00:00');

INSERT INTO userdata (userdata_id, user_id, project_id, created_at) VALUES
	(420471426627371009, 'd539f0b5f4ede5de830a56fd959f74069f383f5a00dc1ffd09c01cd18a2b587b', '15e38c18de014fa1b769f12dba4168f3', '2019-01-25 03:48:16.114126+00:00'),
	(420621331136741377, '9c2ebe8a3664b8cc847b3c61c78c30ba471d87c9110dfb25bbe9250b9aa46e91', 'c8b7b8ee391d40e0a8aef3b5b2860788', '2019-01-25 16:30:43.338558+00:00');

INSERT INTO zn_type (id_type, nm_type) VALUES
	(402140280385142785, 'SOA'),
	(402329131320508417, 'SRV'),
	(402386688803307521, 'A'),
	(402393625286410241, 'NS'),
	(402427533112147969, 'CNAME'),
	(402427545745850369, 'MX'),
	(402427683852124161, 'AAAA'),
	(402427759247851521, 'TXT');

INSERT INTO zn_record (id_record, id_type, id_zone, date_record, nm_record, state) VALUES
	(440099715269754881, 402140280385142785, 440099714981298177, '2019040418', '@', 1),
	(440099715555164161, 402393625286410241, 440099714981298177, '2019040418', '@', 1),
	(440099715692920833, 402427533112147969, 440099714981298177, '2019040418', 'www', 1),
	(440585424647356417, 402140280385142785, 440585424342024193, '2019040611', '@', 1),
	(440585425080090625, 402393625286410241, 440585424342024193, '2019040611', '@', 1),
	(440585425322901505, 402427533112147969, 440585424342024193, '2019040611', 'www', 1),
	(440590527417122817, 402140280385142785, 440590527158648833, '2019040612', '@', 1),
	(440590527745851393, 402393625286410241, 440590527158648833, '2019040612', '@', 1),
	(440590527961235457, 402427533112147969, 440590527158648833, '2019040612', 'www', 1),
	(440591958662578177, 402140280385142785, 440591958449225729, '2019040612', '@', 1),
	(440591959018635265, 402393625286410241, 440591958449225729, '2019040612', '@', 1),
	(440591959197089793, 402427533112147969, 440591958449225729, '2019040612', 'www', 1),
	(440610729152446465, 402386688803307521, 440585424342024193, '2018070410', 'testa', 1);

INSERT INTO zn_content_serial (id_content_serial, id_record, nm_content_serial) VALUES
	(440099715415867393, 440099715269754881, '10800'),
	(440099715446177793, 440099715269754881, '3600'),
	(440099715470786561, 440099715269754881, '604800'),
	(440099715500834817, 440099715269754881, '38400'),
	(440585424860512257, 440585424647356417, '10800'),
	(440585424889413633, 440585424647356417, '3600'),
	(440585424917463041, 440585424647356417, '604800'),
	(440585424946692097, 440585424647356417, '38400'),
	(440590527591677953, 440590527417122817, '10800'),
	(440590527619235841, 440590527417122817, '3600'),
	(440590527646597121, 440590527417122817, '604800'),
	(440590527673139201, 440590527417122817, '38400'),
	(440591958849421313, 440591958662578177, '10800'),
	(440591958875701249, 440591958662578177, '3600'),
	(440591958902407169, 440591958662578177, '604800'),
	(440591958938615809, 440591958662578177, '38400');

INSERT INTO zn_ttl (id_ttl, nm_ttl) VALUES
	(402140815780249601, '86400'),
	(402427897814220801, '43200'),
	(402427936007192577, '28800'),
	(402427994557939713, '14400'),
	(402428031103795201, '7200'),
	(402428067470835713, '3600'),
	(402428102489735169, '1800'),
	(402428115608600577, '900'),
	(402428126292705281, '300');

INSERT INTO zn_ttldata (id_ttldata, id_record, id_ttl, created_at) VALUES
	(440099715313532929, 440099715269754881, 402140815780249601, '2019-04-04 11:42:54.448452+00:00'),
	(440099715594256385, 440099715555164161, 402140815780249601, '2019-04-04 11:42:54.534217+00:00'),
	(440099715723657217, 440099715692920833, 402140815780249601, '2019-04-04 11:42:54.573409+00:00'),
	(440585424723083265, 440585424647356417, 402140815780249601, '2019-04-06 04:53:21.196689+00:00'),
	(440585425162502145, 440585425080090625, 402140815780249601, '2019-04-06 04:53:21.330697+00:00'),
	(440585425354457089, 440585425322901505, 402140815780249601, '2019-04-06 04:53:21.389363+00:00'),
	(440590527478792193, 440590527417122817, 402140815780249601, '2019-04-06 05:19:18.434384+00:00'),
	(440590527804375041, 440590527745851393, 402140815780249601, '2019-04-06 05:19:18.533676+00:00'),
	(440590527995084801, 440590527961235457, 402140815780249601, '2019-04-06 05:19:18.591516+00:00'),
	(440591958721265665, 440591958662578177, 402140815780249601, '2019-04-06 05:26:35.214999+00:00'),
	(440591959064313857, 440591959018635265, 402140815780249601, '2019-04-06 05:26:35.31968+00:00'),
	(440591959223861249, 440591959197089793, 402140815780249601, '2019-04-06 05:26:35.368407+00:00'),
	(440610729958539265, 440610729152446465, 402428031103795201, '2019-04-06 07:02:03.741966+00:00');

INSERT INTO zn_content (id_content, id_ttldata, nm_content) VALUES
	(440099715365437441, 440099715313532929, 'satu.neodns.id.'),
	(440099715391651841, 440099715313532929, 'dua.neodns.id.'),
	(440099715637248001, 440099715594256385, 'satu.neodns.id.'),
	(440099715663527937, 440099715594256385, 'dua.neodns.id.'),
	(440099715754688513, 440099715723657217, 'janda3.com.'),
	(440585424799399937, 440585424723083265, 'satu.neodns.id.'),
	(440585424830496769, 440585424723083265, 'dua.neodns.id.'),
	(440585425259134977, 440585425162502145, 'satu.neodns.id.'),
	(440585425291411457, 440585425162502145, 'dua.neodns.id.'),
	(440585425385947137, 440585425354457089, 'janda4.com.'),
	(440590527535284225, 440590527478792193, 'satu.neodns.id.'),
	(440590527562383361, 440590527478792193, 'dua.neodns.id.'),
	(440590527899467777, 440590527804375041, 'satu.neodns.id.'),
	(440590527929942017, 440590527804375041, 'dua.neodns.id.'),
	(440590528026214401, 440590527995084801, 'gadis1.com.'),
	(440591958773596161, 440591958721265665, 'satu.neodns.id.'),
	(440591958813605889, 440591958721265665, 'dua.neodns.id.'),
	(440591959133159425, 440591959064313857, 'satu.neodns.id.'),
	(440591959157243905, 440591959064313857, 'dua.neodns.id.'),
	(440591959250370561, 440591959223861249, 'gadis2.com.'),
	(440610730840195073, 440610729958539265, '127.0.0.1');

INSERT INTO zn_user_zone (id_user_zone, userdata_id, id_zone) VALUES
	(440099715066265601, 420621331136741377, 440099714981298177),
	(440585424428040193, 420621331136741377, 440585424342024193),
	(440590527295815681, 420621331136741377, 440590527158648833),
	(440591958548316161, 420621331136741377, 440591958449225729);

ALTER TABLE cs_acl_master ADD CONSTRAINT cs_acl_master_zone_fk FOREIGN KEY (id_zone) REFERENCES zn_zone (id_zone) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE cs_acl_master ADD CONSTRAINT cs_acl_master_cs_master_fk FOREIGN KEY (id_master) REFERENCES cs_master (id_master);
ALTER TABLE cs_acl_master_log ADD CONSTRAINT cs_acl_master_log_cs_acl_master_fk FOREIGN KEY (id_acl_master) REFERENCES cs_acl_master (id_acl_master) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE cs_acl_slave ADD CONSTRAINT cs_acl_slave_cs_acl_master_fk FOREIGN KEY (id_acl_master) REFERENCES cs_acl_master (id_acl_master) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE cs_acl_slave ADD CONSTRAINT cs_acl_slave_cs_slave_fk FOREIGN KEY (id_slave) REFERENCES cs_slave (id_slave) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE cs_acl_slave_log ADD CONSTRAINT cs_acl_slave_fk FOREIGN KEY (id_acl_slave) REFERENCES cs_acl_slave (id_acl_slave) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE cs_notify_master ADD CONSTRAINT cs_notify_cs_master_fk FOREIGN KEY (id_master) REFERENCES cs_master (id_master) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE cs_notify_master ADD CONSTRAINT cs_notify_zone_fk FOREIGN KEY (id_zone) REFERENCES zn_zone (id_zone) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE cs_notify_master_log ADD CONSTRAINT cs_notify_master_log_cs_notify_master_fk FOREIGN KEY (id_notify_master) REFERENCES cs_notify_master (id_notify_master) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE cs_notify_slave ADD CONSTRAINT cs_notify_slave_cs_slave_fk FOREIGN KEY (id_slave) REFERENCES cs_slave (id_slave) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE cs_notify_slave ADD CONSTRAINT cs_notify_slave_cs_notify_master_fk FOREIGN KEY (id_notify_master) REFERENCES cs_notify_master (id_notify_master) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE cs_notify_slave_log ADD CONSTRAINT cs_notify_slave_log_cs_notify_slave_fk FOREIGN KEY (id_notify_slave) REFERENCES cs_notify_slave (id_notify_slave) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE zn_record ADD CONSTRAINT fk_id_type_ref_type FOREIGN KEY (id_type) REFERENCES zn_type (id_type) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE zn_record ADD CONSTRAINT fk_id_zone_ref_zone FOREIGN KEY (id_zone) REFERENCES zn_zone (id_zone) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE zn_content_serial ADD CONSTRAINT zn_content_serial_zn_record_fk FOREIGN KEY (id_record) REFERENCES zn_record (id_record) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE zn_ttldata ADD CONSTRAINT fk_id_record_ref_record FOREIGN KEY (id_record) REFERENCES zn_record (id_record) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE zn_ttldata ADD CONSTRAINT fk_id_ttl_ref_ttl FOREIGN KEY (id_ttl) REFERENCES zn_ttl (id_ttl) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE zn_content ADD CONSTRAINT zn_content_zn_ttldata_fk FOREIGN KEY (id_ttldata) REFERENCES zn_ttldata (id_ttldata) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE zn_user_zone ADD CONSTRAINT fk_id_zone_ref_zone FOREIGN KEY (id_zone) REFERENCES zn_zone (id_zone) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE zn_user_zone ADD CONSTRAINT fk_userdata_id_ref FOREIGN KEY (userdata_id) REFERENCES userdata (userdata_id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Validate foreign key constraints. These can fail if there was unvalidated data during the dump.
ALTER TABLE cs_acl_master VALIDATE CONSTRAINT cs_acl_master_zone_fk;
ALTER TABLE cs_acl_master VALIDATE CONSTRAINT cs_acl_master_cs_master_fk;
ALTER TABLE cs_acl_master_log VALIDATE CONSTRAINT cs_acl_master_log_cs_acl_master_fk;
ALTER TABLE cs_acl_slave VALIDATE CONSTRAINT cs_acl_slave_cs_acl_master_fk;
ALTER TABLE cs_acl_slave VALIDATE CONSTRAINT cs_acl_slave_cs_slave_fk;
ALTER TABLE cs_acl_slave_log VALIDATE CONSTRAINT cs_acl_slave_fk;
ALTER TABLE cs_notify_master VALIDATE CONSTRAINT cs_notify_cs_master_fk;
ALTER TABLE cs_notify_master VALIDATE CONSTRAINT cs_notify_zone_fk;
ALTER TABLE cs_notify_master_log VALIDATE CONSTRAINT cs_notify_master_log_cs_notify_master_fk;
ALTER TABLE cs_notify_slave VALIDATE CONSTRAINT cs_notify_slave_cs_slave_fk;
ALTER TABLE cs_notify_slave VALIDATE CONSTRAINT cs_notify_slave_cs_notify_master_fk;
ALTER TABLE cs_notify_slave_log VALIDATE CONSTRAINT cs_notify_slave_log_cs_notify_slave_fk;
ALTER TABLE zn_record VALIDATE CONSTRAINT fk_id_type_ref_type;
ALTER TABLE zn_record VALIDATE CONSTRAINT fk_id_zone_ref_zone;
ALTER TABLE zn_content_serial VALIDATE CONSTRAINT zn_content_serial_zn_record_fk;
ALTER TABLE zn_ttldata VALIDATE CONSTRAINT fk_id_record_ref_record;
ALTER TABLE zn_ttldata VALIDATE CONSTRAINT fk_id_ttl_ref_ttl;
ALTER TABLE zn_content VALIDATE CONSTRAINT zn_content_zn_ttldata_fk;
ALTER TABLE zn_user_zone VALIDATE CONSTRAINT fk_id_zone_ref_zone;
ALTER TABLE zn_user_zone VALIDATE CONSTRAINT fk_userdata_id_ref;
