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
	CONSTRAINT cs_acl_master_pk PRIMARY KEY (id_acl_master ASC),
	INDEX cs_acl_master_auto_index_cs_acl_master_zone_fk (id_zone ASC),
	INDEX cs_acl_master_auto_index_cs_acl_master_cs_master_fk (id_master ASC),
	FAMILY "primary" (id_acl_master, id_zone, id_master, state, create_date)
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

CREATE VIEW v_cs_acl_slave (id_acl_slave, id_acl_master, id_slave, id_zone, ip_slave, nm_slave, port_slave, ip_master, nm_master, port_master, nm_zone) AS SELECT m1.id_acl_slave, m1.id_acl_master, m1.id_slave, m2.id_zone, m3.ip_slave, m3.nm_slave, m3.port AS port_slave, m4.ip_master, m4.nm_master, m4.port AS port_master, m5.nm_zone FROM knotdb.public.cs_acl_slave AS m1 JOIN knotdb.public.cs_acl_master AS m2 ON m1.id_acl_master = m2.id_acl_master JOIN knotdb.public.cs_slave AS m3 ON m1.id_slave = m3.id_slave JOIN knotdb.public.cs_master AS m4 ON m2.id_master = m4.id_master JOIN knotdb.public.zn_zone AS m5 ON m2.id_zone = m5.id_zone;

CREATE VIEW v_cs_notify_master (id_notify_master, id_master, id_zone, nm_zone, state, ip_master, nm_master, port) AS SELECT m1.id_notify_master, m1.id_master, m1.id_zone, m2.nm_zone, m2.state, m3.ip_master, m3.nm_master, m3.port FROM knotdb.public.cs_notify_master AS m1 JOIN knotdb.public.zn_zone AS m2 ON m1.id_zone = m2.id_zone JOIN knotdb.public.cs_master AS m3 ON m1.id_master = m3.id_master;

CREATE VIEW v_cs_notify_slave (id_notify_slave, id_notify_master, id_slave, ip_slave, nm_slave, slave_port, ip_master, nm_master, master_port, id_zone, nm_zone, state) AS SELECT m1.id_notify_slave, m1.id_notify_master, m1.id_slave, m3.ip_slave, m3.nm_slave, m3.port AS slave_port, m4.ip_master, m4.nm_master, m4.port AS master_port, m5.id_zone, m5.nm_zone, m5.state FROM knotdb.public.cs_notify_slave AS m1 JOIN knotdb.public.cs_notify_master AS m2 ON m1.id_notify_master = m2.id_notify_master JOIN knotdb.public.cs_slave AS m3 ON m1.id_slave = m3.id_slave JOIN knotdb.public.cs_master AS m4 ON m2.id_master = m4.id_master JOIN knotdb.public.zn_zone AS m5 ON m2.id_zone = m5.id_zone;

CREATE VIEW v_record (id_record, id_zone, nm_zone, nm_record, date_record, nm_type, state) AS SELECT m1.id_record, m2.id_zone, m2.nm_zone, m1.nm_record, m1.date_record, m3.nm_type, m1.state FROM knotdb.public.zn_record AS m1 JOIN knotdb.public.zn_zone AS m2 ON m1.id_zone = m2.id_zone JOIN knotdb.public.zn_type AS m3 ON m1.id_type = m3.id_type;

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
	(427820188203778049, 'kalkun.com', 1),
	(427820203189272577, 'ayam.com', 1),
	(427821250124644353, 'kambing.com', 1),
	(427863702440640513, 'meongbego.com', 1),
	(427863789571670017, 'riski.com', 1);

INSERT INTO cs_master (id_master, nm_master, ip_master, port) VALUES
	(402152439124393985, 'master1', '127.0.0.1', '6967');

INSERT INTO cs_acl_master (id_acl_master, id_zone, id_master, state, create_date) VALUES
	(440035696139730945, 427820188203778049, 402152439124393985, 0, '2019-04-04 10:56:26.622607+00:00');

INSERT INTO cs_acl_master_log (id_cs_acl_master_log, id_acl_master, messages, command_type, log_date) VALUES
	(440075501029785601, 440035696139730945, e'error: (not exists) zone[kalkun.com].acl = slave1\n', 'acl', '2019-04-04 11:00:52.072842+00:00'),
	(440075732972142593, 440035696139730945, e'error: (not exists) zone[kalkun.com].acl = slave1\n', 'acl', '2019-04-04 11:00:52.072842+00:00'),
	(440076115867336705, 440035696139730945, e'error: (not exists) zone[kalkun.com].acl = slave1\n', 'acl', '2019-04-04 11:00:52.072842+00:00'),
	(440076169721839617, 440035696139730945, e'error: (not exists) zone[kalkun.com].acl = slave1\n', 'acl', '2019-04-04 11:00:52.072842+00:00'),
	(440076227652812801, 440035696139730945, e'error: (not exists) zone[kalkun.com].acl = slave1\n', 'acl', '2019-04-04 11:00:52.072842+00:00'),
	(440076259252142081, 440035696139730945, e'error: (not exists) zone[kalkun.com].acl = slave1\n', 'acl', '2019-04-04 11:00:52.072842+00:00');

INSERT INTO cs_slave (id_slave, nm_slave, ip_slave, port) VALUES
	(402152759030939649, 'slave1', '127.0.0.1', '6967'),
	(402153106273501185, 'slave2', '127.0.0.1', '6967');

INSERT INTO cs_acl_slave (id_acl_slave, id_acl_master, id_slave, state, create_date) VALUES
	(440036862719524865, 440035696139730945, 402152759030939649, 0, '2019-04-04 10:55:14.983594+00:00'),
	(440036862754717697, 440035696139730945, 402153106273501185, 0, '2019-04-04 10:55:14.983594+00:00');

INSERT INTO cs_acl_slave_log (id_cs_slave_log, id_acl_slave, command_type, messages, log_date) VALUES
	(440079785892904961, 440036862719524865, 'add: acl', e'error: (not exists) zone[kalkun.com].acl = notify_from_master\n', '2019-04-04 11:01:16.483834+00:00'),
	(440079786731536385, 440036862754717697, 'add: acl', e'error: (not exists) zone[kalkun.com].acl = notify_from_master\n', '2019-04-04 11:01:16.483834+00:00'),
	(440079901365829633, 440036862719524865, 'add: acl', e'error: (not exists) zone[kalkun.com].acl = notify_from_master\n', '2019-04-04 11:01:16.483834+00:00'),
	(440079902254333953, 440036862754717697, 'add: acl', e'error: (not exists) zone[kalkun.com].acl = notify_from_master\n', '2019-04-04 11:01:16.483834+00:00'),
	(440079949388349441, 440036862719524865, 'add: acl', e'error: (not exists) zone[kalkun.com].acl = notify_from_master\n', '2019-04-04 11:01:16.483834+00:00'),
	(440079950283702273, 440036862754717697, 'add: acl', e'error: (not exists) zone[kalkun.com].acl = notify_from_master\n', '2019-04-04 11:01:16.483834+00:00'),
	(440080054533914625, 440036862719524865, 'add: acl', e'error: (not exists) zone[kalkun.com].acl = notify_from_master\n', '2019-04-04 11:01:16.483834+00:00'),
	(440080055357145089, 440036862754717697, 'add: acl', e'error: (not exists) zone[kalkun.com].acl = notify_from_master\n', '2019-04-04 11:01:16.483834+00:00');

INSERT INTO cs_notify_master (id_notify_master, id_zone, id_master, state, column1) VALUES
	(432940401229987841, 427820188203778049, 402152439124393985, 0, '2019-04-04 10:57:51.070721+00:00');

INSERT INTO cs_notify_master_log (id_cs_master_log, id_notify_master, messages, command_type, log_date) VALUES
	(440076893305667585, 432940401229987841, e'error: (not exists) zone[kalkun.com].notify = slave1\n', 'notify', '2019-04-04 11:01:46.248387+00:00'),
	(440076983512334337, 432940401229987841, e'error: (not exists) zone[kalkun.com].notify = slave1\n', 'notify', '2019-04-04 11:01:46.248387+00:00'),
	(440077241849643009, 432940401229987841, e'error: (not exists) zone[kalkun.com].notify = slave1\n', 'notify', '2019-04-04 11:01:46.248387+00:00'),
	(440077298529959937, 432940401229987841, e'error: (not exists) zone[kalkun.com].notify = slave1\n', 'notify', '2019-04-04 11:01:46.248387+00:00'),
	(440077331121700865, 432940401229987841, e'error: (not exists) zone[kalkun.com].notify = slave1\n', 'notify', '2019-04-04 11:01:46.248387+00:00'),
	(440077686818570241, 432940401229987841, e'error: (not exists) zone[kalkun.com].notify = slave1\n', 'add: notify', '2019-04-04 11:01:46.248387+00:00');

INSERT INTO cs_notify_slave (id_notify_slave, id_notify_master, id_slave, state, create_date) VALUES
	(432940678112247809, 432940401229987841, 402152759030939649, 3, '2019-04-04 10:59:59.850271+00:00'),
	(432940737990656001, 432940401229987841, 402153106273501185, 3, '2019-04-04 10:59:59.850271+00:00');

INSERT INTO cs_notify_slave_log (id_cs_notify_slave_log, id_notify_slave, messages, command_type, log_date) VALUES
	(440078630053347329, 432940678112247809, e'error: (invalid item) zone[kalkun.com].master master1\n', 'add: notify', '2019-04-04 11:02:21.027779+00:00'),
	(440078630943391745, 432940737990656001, e'error: (invalid item) zone[kalkun.com].master master1\n', 'add: notify', '2019-04-04 11:02:21.027779+00:00'),
	(440078792802729985, 432940678112247809, e'error: (invalid item) zone[kalkun.com].master master1\n', 'add: notify', '2019-04-04 11:02:21.027779+00:00'),
	(440078793704374273, 432940737990656001, e'error: (invalid item) zone[kalkun.com].master master1\n', 'add: notify', '2019-04-04 11:02:21.027779+00:00');

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
	(427820188554035201, 402140280385142785, 427820188203778049, '2019022009', 'kalkun.com', 1),
	(427820188954656769, 402393625286410241, 427820188203778049, '2019022009', '@', 1),
	(427820189143334913, 402427533112147969, 427820188203778049, '2019022009', 'www', 1),
	(427820203379589121, 402140280385142785, 427820203189272577, '2019022009', 'ayam.com', 1),
	(427820203772379137, 402393625286410241, 427820203189272577, '2019022009', '@', 1),
	(427820203964071937, 402427533112147969, 427820203189272577, '2019022009', 'www', 1),
	(427821250294480897, 402140280385142785, 427821250124644353, '2019022009', '@', 1),
	(427821250687041537, 402393625286410241, 427821250124644353, '2019022009', '@', 1),
	(427821250925690881, 402427533112147969, 427821250124644353, '2019022009', 'www', 1),
	(427829589685764097, 402427533112147969, 427821250124644353, '2018070410', 'www', 1),
	(427837747447496705, 402427545745850369, 427821250124644353, '2018070410', 'www', 1),
	(427838394454933505, 402427545745850369, 427821250124644353, '2018070410', 'www', 1),
	(427839493441519617, 402427545745850369, 427821250124644353, '2018070410', 'www', 1),
	(427845547936940033, 402427533112147969, 427821250124644353, '2018070410', 'www', 1),
	(427863702794076161, 402140280385142785, 427863702440640513, '2019022013', '@', 1),
	(427863703274061825, 402393625286410241, 427863702440640513, '2019022013', '@', 1),
	(427863703469457409, 402427533112147969, 427863702440640513, '2019022013', 'www', 1),
	(427863789787086849, 402140280385142785, 427863789571670017, '2019022013', '@', 1),
	(427863790162706433, 402393625286410241, 427863789571670017, '2019022013', '@', 1),
	(427863790390870017, 402427533112147969, 427863789571670017, '2019022013', 'www', 1);

INSERT INTO zn_content_serial (id_content_serial, id_record, nm_content_serial) VALUES
	(427820188785082369, 427820188554035201, '10800'),
	(427820188814147585, 427820188554035201, '3600'),
	(427820188841050113, 427820188554035201, '604800'),
	(427820188868902913, 427820188554035201, '38400'),
	(427820203575410689, 427820203379589121, '10800'),
	(427820203606048769, 427820203379589121, '3600'),
	(427820203635441665, 427820203379589121, '604800'),
	(427820203669979137, 427820203379589121, '38400'),
	(427821250486435841, 427821250294480897, '10800'),
	(427821250516484097, 427821250294480897, '3600'),
	(427821250546368513, 427821250294480897, '604800'),
	(427821250575466497, 427821250294480897, '38400'),
	(427838187309400065, 427837747447496705, 'kambing.com.'),
	(427838396088025089, 427838394454933505, 'kerbau.com.'),
	(427839495158071297, 427839493441519617, 'ayam.com.'),
	(427863703041212417, 427863702794076161, '10800'),
	(427863703074439169, 427863702794076161, '3600'),
	(427863703106781185, 427863702794076161, '604800'),
	(427863703141318657, 427863702794076161, '38400'),
	(427863789961084929, 427863789787086849, '10800'),
	(427863789989396481, 427863789787086849, '3600'),
	(427863790017544193, 427863789787086849, '604800'),
	(427863790047002625, 427863789787086849, '38400');

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
	(427820188633858049, 427820188554035201, 402140815780249601, '2019-02-20 02:46:00.300104+00:00'),
	(427820189012819969, 427820188954656769, 402140815780249601, '2019-02-20 02:46:00.416106+00:00'),
	(427820189170958337, 427820189143334913, 402140815780249601, '2019-02-20 02:46:00.464415+00:00'),
	(427820203449483265, 427820203379589121, 402140815780249601, '2019-02-20 02:46:04.821705+00:00'),
	(427820203825266689, 427820203772379137, 402140815780249601, '2019-02-20 02:46:04.936621+00:00'),
	(427820203990876161, 427820203964071937, 402140815780249601, '2019-02-20 02:46:04.987137+00:00'),
	(427821250349268993, 427821250294480897, 402140815780249601, '2019-02-20 02:51:24.310446+00:00'),
	(427821250784067585, 427821250687041537, 402140815780249601, '2019-02-20 02:51:24.442871+00:00'),
	(427821250955378689, 427821250925690881, 402140815780249601, '2019-02-20 02:51:24.495221+00:00'),
	(427829590105128961, 427829589685764097, 402428031103795201, '2019-02-20 03:33:49.401906+00:00'),
	(427837747893895169, 427837747447496705, 402428031103795201, '2019-02-20 04:15:18.961461+00:00'),
	(427838394890846209, 427838394454933505, 402428031103795201, '2019-02-20 04:18:36.409167+00:00'),
	(427839493905580033, 427839493441519617, 402428031103795201, '2019-02-20 04:24:11.802025+00:00'),
	(427845548297617409, 427845547936940033, 402428031103795201, '2019-02-20 04:54:59.455753+00:00'),
	(427863702886285313, 427863702794076161, 402140815780249601, '2019-02-20 06:27:19.796205+00:00'),
	(427863703336943617, 427863703274061825, 402140815780249601, '2019-02-20 06:27:19.933992+00:00'),
	(427863703499505665, 427863703469457409, 402140815780249601, '2019-02-20 06:27:19.983575+00:00'),
	(427863789847478273, 427863789787086849, 402140815780249601, '2019-02-20 06:27:46.334951+00:00'),
	(427863790239449089, 427863790162706433, 402140815780249601, '2019-02-20 06:27:46.454403+00:00'),
	(427863790424489985, 427863790390870017, 402140815780249601, '2019-02-20 06:27:46.510786+00:00');

INSERT INTO zn_content (id_content, id_ttldata, nm_content) VALUES
	(427820188711223297, 427820188633858049, 'satu.neodns.id.'),
	(427820188740321281, 427820188633858049, 'dua.neodns.id.'),
	(427820189086744577, 427820189012819969, 'satu.neodns.id.'),
	(427820189115645953, 427820189012819969, 'dua.neodns.id.'),
	(427820189199171585, 427820189170958337, 'kalkun.com.'),
	(427820203518820353, 427820203449483265, 'satu.neodns.id.'),
	(427820203546574849, 427820203449483265, 'dua.neodns.id.'),
	(427820203910430721, 427820203825266689, 'satu.neodns.id.'),
	(427820203937300481, 427820203825266689, 'dua.neodns.id.'),
	(427820204016992257, 427820203990876161, 'ayam.com.'),
	(427821250432499713, 427821250349268993, 'satu.neodns.id.'),
	(427821250456715265, 427821250349268993, 'dua.neodns.id.'),
	(427821250868084737, 427821250784067585, 'satu.neodns.id.'),
	(427821250896691201, 427821250784067585, 'dua.neodns.id.'),
	(427821250985754625, 427821250955378689, 'kambing.com.'),
	(427829590611722241, 427829590105128961, 'ayam.com.'),
	(427837748730068993, 427837747893895169, '0'),
	(427838395660435457, 427838394890846209, '0'),
	(427839494791528449, 427839493905580033, '0'),
	(427845548751552513, 427845548297617409, 'ayam.com.'),
	(427863702972956673, 427863702886285313, 'satu.neodns.id.'),
	(427863703006904321, 427863702886285313, 'dua.neodns.id.'),
	(427863703409426433, 427863703336943617, 'satu.neodns.id.'),
	(427863703438983169, 427863703336943617, 'dua.neodns.id.'),
	(427863703530471425, 427863703499505665, 'meongbego.com.'),
	(427863789906362369, 427863789847478273, 'satu.neodns.id.'),
	(427863789933559809, 427863789847478273, 'dua.neodns.id.'),
	(427863790328709121, 427863790239449089, 'satu.neodns.id.'),
	(427863790359838721, 427863790239449089, 'dua.neodns.id.'),
	(427863790456373249, 427863790424489985, 'riski.com.');

INSERT INTO zn_user_zone (id_user_zone, userdata_id, id_zone) VALUES
	(427820188361981953, 420621331136741377, 427820188203778049),
	(427820203258478593, 420621331136741377, 427820203189272577),
	(427821250209644545, 420621331136741377, 427821250124644353),
	(427863702590259201, 420621331136741377, 427863702440640513),
	(427863789659258881, 420621331136741377, 427863789571670017);

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
