CREATE TABLE zn_zone (
	id_zone INT8 NOT NULL DEFAULT unique_rowid(),
	nm_zone STRING(200) NULL,
	state INT8 NULL DEFAULT 0:::INT8,
	counter INT8 NOT NULL DEFAULT 0:::INT8,
	CONSTRAINT "primary" PRIMARY KEY (id_zone ASC),
	UNIQUE INDEX zone_zone_name_key (nm_zone ASC),
	FAMILY "primary" (id_zone, nm_zone, state, counter)
);

CREATE TABLE cs_master (
	id_master INT8 NOT NULL DEFAULT unique_rowid(),
	nm_master STRING NULL,
	ip_master STRING NULL,
	port STRING NULL DEFAULT '53':::STRING,
	nm_config VARCHAR NULL,
	CONSTRAINT master_pk PRIMARY KEY (id_master ASC),
	UNIQUE INDEX cs_master_un (nm_master ASC),
	FAMILY "primary" (id_master, nm_master, ip_master, port, nm_config)
);

CREATE TABLE cs_acl_master (
	id_acl_master INT8 NOT NULL DEFAULT unique_rowid(),
	id_zone INT8 NULL,
	id_master INT8 NULL,
	state INT8 NOT NULL DEFAULT 0:::INT8,
	create_date TIMESTAMPTZ NOT NULL DEFAULT now():::TIMESTAMPTZ,
	nm_acl VARCHAR NULL,
	CONSTRAINT cs_acl_master_pk PRIMARY KEY (id_acl_master ASC),
	INDEX cs_acl_master_auto_index_cs_acl_master_zone_fk (id_zone ASC),
	INDEX cs_acl_master_auto_index_cs_acl_master_cs_master_fk (id_master ASC),
	FAMILY "primary" (id_acl_master, id_zone, id_master, state, create_date, nm_acl)
);

CREATE TABLE cs_acl_master_log (
	id_cs_acl_master_log INT8 NOT NULL DEFAULT unique_rowid(),
	id_acl_master INT8 NOT NULL,
	messages VARCHAR NULL,
	command_type VARCHAR NULL,
	log_date TIMESTAMPTZ NOT NULL DEFAULT now():::TIMESTAMPTZ,
	CONSTRAINT cs_acl_master_log_pk PRIMARY KEY (id_cs_acl_master_log ASC),
	INDEX cs_acl_master_log_auto_index_cs_acl_master_log_cs_acl_master_fk (id_acl_master ASC),
	FAMILY "primary" (id_cs_acl_master_log, id_acl_master, messages, command_type, log_date)
);

CREATE TABLE cs_slave (
	id_slave INT8 NOT NULL DEFAULT unique_rowid(),
	nm_slave STRING NULL,
	ip_slave STRING NULL,
	port STRING NULL DEFAULT '53':::STRING,
	CONSTRAINT "primary" PRIMARY KEY (id_slave ASC),
	UNIQUE INDEX cs_slave_un (nm_slave ASC),
	FAMILY "primary" (id_slave, nm_slave, ip_slave, port)
);

CREATE TABLE cs_acl_slave (
	id_acl_slave INT8 NOT NULL DEFAULT unique_rowid(),
	id_acl_master INT8 NULL,
	id_slave INT8 NULL,
	state INT8 NULL DEFAULT 0:::INT8,
	create_date TIMESTAMPTZ NOT NULL DEFAULT now():::TIMESTAMPTZ,
	CONSTRAINT cs_acl_slave_pk PRIMARY KEY (id_acl_slave ASC),
	INDEX cs_acl_slave_auto_index_cs_acl_slave_cs_acl_master_fk (id_acl_master ASC),
	INDEX cs_acl_slave_auto_index_cs_acl_slave_cs_slave_fk (id_slave ASC),
	FAMILY "primary" (id_acl_slave, id_acl_master, id_slave, state, create_date)
);

CREATE TABLE cs_acl_slave_log (
	id_cs_slave_log INT8 NOT NULL DEFAULT unique_rowid(),
	id_acl_slave INT8 NOT NULL,
	command_type VARCHAR NULL,
	messages VARCHAR NULL,
	log_date TIMESTAMPTZ NOT NULL DEFAULT now():::TIMESTAMPTZ,
	CONSTRAINT "primary" PRIMARY KEY (id_cs_slave_log ASC),
	INDEX cs_acl_slave_log_auto_index_cs_acl_slave_fk (id_acl_slave ASC),
	FAMILY "primary" (id_cs_slave_log, id_acl_slave, command_type, messages, log_date)
);

CREATE TABLE cs_notify_master (
	id_notify_master INT8 NOT NULL DEFAULT unique_rowid(),
	id_zone INT8 NULL,
	id_master INT8 NULL,
	state INT8 NOT NULL DEFAULT 0:::INT8,
	column1 TIMESTAMPTZ NOT NULL DEFAULT now():::TIMESTAMPTZ,
	CONSTRAINT cs_notify_pk PRIMARY KEY (id_notify_master ASC),
	INDEX cs_notify_auto_index_cs_notify_cs_master_fk (id_master ASC),
	INDEX cs_notify_auto_index_cs_notify_zone_fk (id_zone ASC),
	FAMILY "primary" (id_notify_master, id_zone, id_master, state, column1)
);

CREATE TABLE cs_notify_master_log (
	id_cs_master_log INT8 NOT NULL DEFAULT unique_rowid(),
	id_notify_master INT8 NOT NULL,
	messages VARCHAR NULL,
	command_type VARCHAR NULL,
	log_date TIMESTAMPTZ NOT NULL DEFAULT now():::TIMESTAMPTZ,
	CONSTRAINT cs_notify_master_log_pk PRIMARY KEY (id_cs_master_log ASC),
	INDEX cs_notify_master_log_auto_index_cs_notify_master_log_cs_notify_master_fk (id_notify_master ASC),
	FAMILY "primary" (id_cs_master_log, id_notify_master, messages, command_type, log_date)
);

CREATE TABLE cs_notify_slave (
	id_notify_slave INT8 NOT NULL DEFAULT unique_rowid(),
	id_notify_master INT8 NULL,
	id_slave INT8 NULL,
	state INT8 NOT NULL DEFAULT 0:::INT8,
	create_date TIMESTAMPTZ NOT NULL DEFAULT now():::TIMESTAMPTZ,
	CONSTRAINT cs_notify_slave_pk PRIMARY KEY (id_notify_slave ASC),
	INDEX cs_notify_slave_auto_index_cs_notify_slave_cs_slave_fk (id_slave ASC),
	INDEX cs_notify_slave_auto_index_cs_notify_slave_cs_notify_master_fk (id_notify_master ASC),
	FAMILY "primary" (id_notify_slave, id_notify_master, id_slave, state, create_date)
);

CREATE TABLE cs_notify_slave_log (
	id_cs_notify_slave_log INT8 NOT NULL DEFAULT unique_rowid(),
	id_notify_slave INT8 NOT NULL,
	messages VARCHAR NULL,
	command_type VARCHAR NULL,
	log_date TIMESTAMPTZ NOT NULL DEFAULT now():::TIMESTAMPTZ,
	CONSTRAINT cs_notify_slave_log_pk PRIMARY KEY (id_cs_notify_slave_log ASC),
	INDEX cs_notify_slave_log_auto_index_cs_notify_slave_log_cs_notify_slave_fk (id_notify_slave ASC),
	FAMILY "primary" (id_cs_notify_slave_log, id_notify_slave, messages, command_type, log_date)
);

CREATE TABLE cs_slave_node (
	id_cs_slave_node INT8 NOT NULL DEFAULT unique_rowid(),
	id_master INT8 NULL,
	nm_slave_node VARCHAR NULL,
	ip_slave_node VARCHAR NULL,
	port_slave_node VARCHAR NULL,
	CONSTRAINT "primary" PRIMARY KEY (id_cs_slave_node ASC),
	INDEX cs_slave_node_auto_index_cs_id_master_fk (id_master ASC),
	FAMILY "primary" (id_cs_slave_node, id_master, nm_slave_node, ip_slave_node, port_slave_node)
);

CREATE TABLE userdata (
	userdata_id INT8 NOT NULL DEFAULT unique_rowid(),
	user_id STRING NOT NULL,
	project_id STRING(100) NOT NULL,
	created_at TIMESTAMP NULL DEFAULT current_timestamp():::TIMESTAMP,
	CONSTRAINT "primary" PRIMARY KEY (userdata_id ASC),
	UNIQUE INDEX userdata_user_id_key (user_id ASC),
	FAMILY "primary" (userdata_id, user_id, project_id, created_at)
);

CREATE TABLE zn_type (
	id_type INT8 NOT NULL DEFAULT unique_rowid(),
	nm_type STRING(100) NULL,
	CONSTRAINT "primary" PRIMARY KEY (id_type ASC),
	UNIQUE INDEX zn_type_un (nm_type ASC),
	FAMILY "primary" (id_type, nm_type)
);

CREATE TABLE zn_record (
	id_record INT8 NOT NULL DEFAULT unique_rowid(),
	id_type INT8 NULL,
	id_zone INT8 NULL,
	date_record STRING(200) NULL,
	nm_record STRING(200) NULL,
	state INT8 NULL DEFAULT 0:::INT8,
	CONSTRAINT "primary" PRIMARY KEY (id_record ASC),
	INDEX record_auto_index_fk_id_type_ref_type (id_type ASC),
	INDEX record_auto_index_fk_id_zone_ref_zone (id_zone ASC),
	FAMILY "primary" (id_record, id_type, id_zone, date_record, nm_record, state)
);

CREATE TABLE zn_content_serial (
	id_content_serial INT8 NOT NULL DEFAULT unique_rowid(),
	id_record INT8 NULL,
	nm_content_serial STRING NULL,
	CONSTRAINT zn_content_serial_pk PRIMARY KEY (id_content_serial ASC),
	INDEX zn_content_serial_auto_index_zn_content_serial_zn_record_fk (id_record ASC),
	FAMILY "primary" (id_content_serial, id_record, nm_content_serial)
);

CREATE VIEW v_content_serial (id_content_serial, id_zone, nm_zone, nm_record, id_record, nm_type, nm_content_serial) AS SELECT m1.id_content_serial, m3.id_zone, m3.nm_zone, m2.nm_record, m2.id_record, m4.nm_type, m1.nm_content_serial FROM knotdb.public.zn_content_serial AS m1 JOIN knotdb.public.zn_record AS m2 ON m1.id_record = m2.id_record JOIN knotdb.public.zn_zone AS m3 ON m2.id_zone = m3.id_zone JOIN knotdb.public.zn_type AS m4 ON m2.id_type = m4.id_type;

CREATE TABLE zn_ttl (
	id_ttl INT8 NOT NULL DEFAULT unique_rowid(),
	nm_ttl STRING(50) NULL,
	CONSTRAINT "primary" PRIMARY KEY (id_ttl ASC),
	UNIQUE INDEX zn_ttl_un (nm_ttl ASC),
	FAMILY "primary" (id_ttl, nm_ttl)
);

CREATE TABLE zn_ttldata (
	id_ttldata INT8 NOT NULL DEFAULT unique_rowid(),
	id_record INT8 NOT NULL,
	id_ttl INT8 NOT NULL,
	created_at TIMESTAMP NULL DEFAULT current_timestamp():::TIMESTAMP,
	CONSTRAINT "primary" PRIMARY KEY (id_ttldata ASC),
	INDEX ttldata_auto_index_fk_id_record_ref_record (id_record ASC),
	INDEX ttldata_auto_index_fk_id_ttl_ref_ttl (id_ttl ASC),
	FAMILY "primary" (id_ttldata, id_record, id_ttl, created_at)
);

CREATE TABLE zn_content (
	id_content INT8 NOT NULL DEFAULT unique_rowid(),
	id_ttldata INT8 NULL,
	nm_content STRING NULL,
	CONSTRAINT zn_content_pk PRIMARY KEY (id_content ASC),
	INDEX zn_content_auto_index_zn_content_zn_ttldata_fk (id_ttldata ASC),
	FAMILY "primary" (id_content, id_ttldata, nm_content)
);

CREATE VIEW v_contentdata (id_content, id_zone, nm_zone, id_record, nm_record, nm_type, nm_ttl, nm_content) AS SELECT m1.id_content, m5.id_zone, m5.nm_zone, m3.id_record, m3.nm_record, m6.nm_type, m4.nm_ttl, m1.nm_content FROM knotdb.public.zn_content AS m1 JOIN knotdb.public.zn_ttldata AS m2 ON m1.id_ttldata = m2.id_ttldata JOIN knotdb.public.zn_record AS m3 ON m2.id_record = m3.id_record JOIN knotdb.public.zn_ttl AS m4 ON m2.id_ttl = m4.id_ttl JOIN knotdb.public.zn_type AS m6 ON m3.id_type = m6.id_type JOIN knotdb.public.zn_zone AS m5 ON m3.id_zone = m5.id_zone;

CREATE VIEW v_cs_acl_master (id_acl_master, id_master, id_zone, nm_zone, ip_master, nm_master, port, nm_config) AS SELECT m1.id_acl_master, m1.id_master, m1.id_zone, m2.nm_zone, m3.ip_master, m3.nm_master, m3.port, m3.nm_config FROM knotdb.public.cs_acl_master AS m1 JOIN knotdb.public.zn_zone AS m2 ON m1.id_zone = m2.id_zone JOIN knotdb.public.cs_master AS m3 ON m1.id_master = m3.id_master;

CREATE VIEW v_cs_acl_slave (id_acl_slave, id_acl_master, id_slave, state, id_zone, ip_slave, nm_slave, port_slave, ip_master, nm_master, port_master, nm_zone) AS SELECT m1.id_acl_slave, m1.id_acl_master, m1.id_slave, m1.state, m2.id_zone, m3.ip_slave, m3.nm_slave, m3.port AS port_slave, m4.ip_master, m4.nm_master, m4.port AS port_master, m5.nm_zone FROM knotdb.public.cs_acl_slave AS m1 JOIN knotdb.public.cs_acl_master AS m2 ON m1.id_acl_master = m2.id_acl_master JOIN knotdb.public.cs_slave AS m3 ON m1.id_slave = m3.id_slave JOIN knotdb.public.cs_master AS m4 ON m2.id_master = m4.id_master JOIN knotdb.public.zn_zone AS m5 ON m2.id_zone = m5.id_zone;

CREATE VIEW v_cs_notify_master (id_notify_master, id_master, id_zone, nm_zone, state, ip_master, nm_master, port) AS SELECT m1.id_notify_master, m1.id_master, m1.id_zone, m2.nm_zone, m2.state, m3.ip_master, m3.nm_master, m3.port FROM knotdb.public.cs_notify_master AS m1 JOIN knotdb.public.zn_zone AS m2 ON m1.id_zone = m2.id_zone JOIN knotdb.public.cs_master AS m3 ON m1.id_master = m3.id_master;

CREATE VIEW v_cs_notify_slave (id_notify_slave, id_notify_master, id_slave, ip_slave, nm_slave, slave_port, ip_master, nm_master, master_port, id_zone, nm_zone, state) AS SELECT m1.id_notify_slave, m1.id_notify_master, m1.id_slave, m3.ip_slave, m3.nm_slave, m3.port AS slave_port, m4.ip_master, m4.nm_master, m4.port AS master_port, m5.id_zone, m5.nm_zone, m5.state FROM knotdb.public.cs_notify_slave AS m1 JOIN knotdb.public.cs_notify_master AS m2 ON m1.id_notify_master = m2.id_notify_master JOIN knotdb.public.cs_slave AS m3 ON m1.id_slave = m3.id_slave JOIN knotdb.public.cs_master AS m4 ON m2.id_master = m4.id_master JOIN knotdb.public.zn_zone AS m5 ON m2.id_zone = m5.id_zone;

CREATE VIEW v_cs_slave_node (id_cs_slave_node, id_master, nm_slave_node, ip_slave_node, port_slave_node, ip_master, nm_config, master_port) AS SELECT m1.id_cs_slave_node, m1.id_master, m1.nm_slave_node, m1.ip_slave_node, m1.port_slave_node, m2.ip_master, m2.nm_config, m2.port AS master_port FROM knotdb.public.cs_slave_node AS m1 JOIN knotdb.public.cs_master AS m2 ON m1.id_master = m2.id_master;

CREATE VIEW v_record (id_record, id_zone, nm_zone, nm_record, date_record, nm_type, state, counter) AS SELECT m1.id_record, m2.id_zone, m2.nm_zone, m1.nm_record, m1.date_record, m3.nm_type, m1.state, m2.counter FROM knotdb.public.zn_record AS m1 JOIN knotdb.public.zn_zone AS m2 ON m1.id_zone = m2.id_zone JOIN knotdb.public.zn_type AS m3 ON m1.id_type = m3.id_type;

CREATE VIEW v_share_zone_record (id_acl_slave, id_acl_master, id_slave, id_record, id_type, state, id_zone, ip_slave, nm_slave, port_slave, ip_master, nm_master, port_master, nm_zone, nm_record, date_record, state_record, nm_type) AS SELECT m1.id_acl_slave, m1.id_acl_master, m1.id_slave, m6.id_record, m7.id_type, m1.state, m2.id_zone, m3.ip_slave, m3.nm_slave, m3.port AS port_slave, m4.ip_master, m4.nm_master, m4.port AS port_master, m5.nm_zone, m6.nm_record, m6.date_record, m6.state AS state_record, m7.nm_type FROM knotdb.public.cs_acl_slave AS m1 JOIN knotdb.public.cs_acl_master AS m2 ON m1.id_acl_master = m2.id_acl_master JOIN knotdb.public.cs_slave AS m3 ON m1.id_slave = m3.id_slave JOIN knotdb.public.cs_master AS m4 ON m2.id_master = m4.id_master JOIN knotdb.public.zn_zone AS m5 ON m2.id_zone = m5.id_zone JOIN knotdb.public.zn_record AS m6 ON m5.id_zone = m6.id_zone JOIN knotdb.public.zn_type AS m7 ON m6.id_type = m7.id_type;

CREATE VIEW v_ttldata (id_ttldata, id_ttl, id_record, id_zone, nm_zone, nm_record, nm_ttl, nm_type) AS SELECT m1.id_ttldata, m1.id_ttl, m2.id_record, m4.id_zone, m4.nm_zone, m2.nm_record, m3.nm_ttl, m5.nm_type FROM knotdb.public.zn_ttldata AS m1 JOIN knotdb.public.zn_record AS m2 ON m1.id_record = m2.id_record JOIN knotdb.public.zn_ttl AS m3 ON m1.id_ttl = m3.id_ttl JOIN knotdb.public.zn_zone AS m4 ON m2.id_zone = m4.id_zone JOIN knotdb.public.zn_type AS m5 ON m2.id_type = m5.id_type;

CREATE TABLE zn_user_zone (
	id_user_zone INT8 NOT NULL DEFAULT unique_rowid(),
	userdata_id INT8 NOT NULL,
	id_zone INT8 NOT NULL,
	CONSTRAINT "primary" PRIMARY KEY (id_user_zone ASC),
	UNIQUE INDEX zn_user_zone_id_zone_key (id_zone ASC),
	INDEX user_zone_auto_index_fk_userdata_id_ref (userdata_id ASC),
	INDEX user_zone_auto_index_fk_id_zone_ref_zone (id_zone ASC),
	FAMILY "primary" (id_user_zone, userdata_id, id_zone)
);

CREATE VIEW v_userzone (id_user_zone, userdata_id, id_zone, user_id, project_id, nm_zone, state) AS SELECT m1.id_user_zone, m2.userdata_id, m3.id_zone, m2.user_id, m2.project_id, m3.nm_zone, m3.state FROM knotdb.public.zn_user_zone AS m1 JOIN knotdb.public.userdata AS m2 ON m1.userdata_id = m2.userdata_id JOIN knotdb.public.zn_zone AS m3 ON m3.id_zone = m1.id_zone;

INSERT INTO zn_zone (id_zone, nm_zone, state, counter) VALUES
	(462973901134430209, 'lagi39.id', 1, 2);

INSERT INTO cs_master (id_master, nm_master, ip_master, port, nm_config) VALUES
	(402152439124393985, 'cmg01z00knms001', '127.0.0.1', '6967', 'cmg'),
	(461914324975517697, 'jkt01z00knms001', '127.0.0.1', '6967', 'jkt');

INSERT INTO cs_slave (id_slave, nm_slave, ip_slave, port) VALUES
	(461914762643046401, 'jkt01z00knsl001', '10.30.4.54', '6967'),
	(461914874332020737, 'cmg01z00knsl001', '10.10.4.54', '6967');

INSERT INTO cs_slave_node (id_cs_slave_node, id_master, nm_slave_node, ip_slave_node, port_slave_node) VALUES
	(461938251232804865, 402152439124393985, 'cmg01z00knsl001', '127.0.0.1', '6967'),
	(461938251266490369, 461914324975517697, 'jkt01z00knsl001', '127.0.0.1', '6967');

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
	(462973901343719425, 402140280385142785, 462973901134430209, '20190624', '@', 1),
	(462973901983907841, 402393625286410241, 462973901134430209, '20190624', '@', 1),
	(462973902385348609, 402427533112147969, 462973901134430209, '20190624', 'www', 1);

INSERT INTO zn_content_serial (id_content_serial, id_record, nm_content_serial) VALUES
	(462973901587611649, 462973901343719425, '10800'),
	(462973901649641473, 462973901343719425, '3600'),
	(462973901715865601, 462973901343719425, '604800'),
	(462973901780058113, 462973901343719425, '38400');

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
	(462973901412794369, 462973901343719425, 402140815780249601, '2019-06-24 06:47:02.061771+00:00'),
	(462973902114488321, 462973901983907841, 402140815780249601, '2019-06-24 06:47:02.275236+00:00'),
	(462973902451998721, 462973902385348609, 402140815780249601, '2019-06-24 06:47:02.378163+00:00');

INSERT INTO zn_content (id_content, id_ttldata, nm_content) VALUES
	(462973901478559745, 462973901412794369, 'satu.neodns.id.'),
	(462973901527777281, 462973901412794369, 'hostmaster.neodns.id.'),
	(462973902254276609, 462973902114488321, 'satu.neodns.id.'),
	(462973902319288321, 462973902114488321, 'dua.neodns.id.'),
	(462973902519009281, 462973902451998721, 'lagi39.id.');

INSERT INTO zn_user_zone (id_user_zone, userdata_id, id_zone) VALUES
	(462973901227819009, 420621331136741377, 462973901134430209);

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
ALTER TABLE cs_slave_node ADD CONSTRAINT cs_id_master_fk FOREIGN KEY (id_master) REFERENCES cs_master (id_master) ON DELETE CASCADE ON UPDATE CASCADE;
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
ALTER TABLE cs_slave_node VALIDATE CONSTRAINT cs_id_master_fk;
ALTER TABLE zn_record VALIDATE CONSTRAINT fk_id_type_ref_type;
ALTER TABLE zn_record VALIDATE CONSTRAINT fk_id_zone_ref_zone;
ALTER TABLE zn_content_serial VALIDATE CONSTRAINT zn_content_serial_zn_record_fk;
ALTER TABLE zn_ttldata VALIDATE CONSTRAINT fk_id_record_ref_record;
ALTER TABLE zn_ttldata VALIDATE CONSTRAINT fk_id_ttl_ref_ttl;
ALTER TABLE zn_content VALIDATE CONSTRAINT zn_content_zn_ttldata_fk;
ALTER TABLE zn_user_zone VALIDATE CONSTRAINT fk_id_zone_ref_zone;
ALTER TABLE zn_user_zone VALIDATE CONSTRAINT fk_userdata_id_ref;
