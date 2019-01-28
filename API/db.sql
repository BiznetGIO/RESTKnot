CREATE TABLE zn_zone (
	id_zone INT NULL DEFAULT unique_rowid(),
	nm_zone STRING(200) NULL,
	CONSTRAINT "primary" PRIMARY KEY (id_zone ASC),
	UNIQUE INDEX zone_zone_name_key (nm_zone ASC),
	FAMILY "primary" (id_zone, nm_zone)
);

CREATE TABLE cs_master (
	id_master INT NOT NULL DEFAULT unique_rowid(),
	nm_master STRING NULL,
	ip_master STRING NULL,
	port STRING NULL DEFAULT '53',
	CONSTRAINT master_pk PRIMARY KEY (id_master ASC),
	UNIQUE INDEX cs_master_un (nm_master ASC),
	FAMILY "primary" (id_master, nm_master, ip_master, port)
);

CREATE TABLE cs_acl_master (
	id_acl_master INT NOT NULL DEFAULT unique_rowid(),
	id_zone INT NULL,
	id_master INT NULL,
	CONSTRAINT cs_acl_master_pk PRIMARY KEY (id_acl_master ASC),
	CONSTRAINT cs_acl_master_zone_fk FOREIGN KEY (id_zone) REFERENCES zn_zone (id_zone) ON DELETE CASCADE ON UPDATE CASCADE,
	INDEX cs_acl_master_auto_index_cs_acl_master_zone_fk (id_zone ASC),
	CONSTRAINT cs_acl_master_cs_master_fk FOREIGN KEY (id_master) REFERENCES cs_master (id_master),
	INDEX cs_acl_master_auto_index_cs_acl_master_cs_master_fk (id_master ASC),
	FAMILY "primary" (id_acl_master, id_zone, id_master)
);

CREATE TABLE cs_slave (
	id_slave INT NOT NULL DEFAULT unique_rowid(),
	nm_slave STRING NULL,
	ip_slave STRING NULL,
	port STRING NULL DEFAULT '53',
	CONSTRAINT "primary" PRIMARY KEY (id_slave ASC),
	UNIQUE INDEX cs_slave_un (nm_slave ASC),
	FAMILY "primary" (id_slave, nm_slave, ip_slave, port)
);

CREATE TABLE cs_acl_slave (
	id_acl_slave INT NOT NULL DEFAULT unique_rowid(),
	id_acl_master INT NULL,
	id_slave INT NULL,
	CONSTRAINT cs_acl_slave_pk PRIMARY KEY (id_acl_slave ASC),
	CONSTRAINT cs_acl_slave_cs_acl_master_fk FOREIGN KEY (id_acl_master) REFERENCES cs_acl_master (id_acl_master) ON DELETE CASCADE ON UPDATE CASCADE,
	INDEX cs_acl_slave_auto_index_cs_acl_slave_cs_acl_master_fk (id_acl_master ASC),
	CONSTRAINT cs_acl_slave_cs_slave_fk FOREIGN KEY (id_slave) REFERENCES cs_slave (id_slave) ON DELETE CASCADE ON UPDATE CASCADE,
	INDEX cs_acl_slave_auto_index_cs_acl_slave_cs_slave_fk (id_slave ASC),
	FAMILY "primary" (id_acl_slave, id_acl_master, id_slave)
);

CREATE TABLE cs_notify_master (
	id_notify_master INT NOT NULL DEFAULT unique_rowid(),
	id_zone INT NULL,
	id_master INT NULL,
	CONSTRAINT cs_notify_pk PRIMARY KEY (id_notify_master ASC),
	CONSTRAINT cs_notify_cs_master_fk FOREIGN KEY (id_master) REFERENCES cs_master (id_master) ON DELETE CASCADE ON UPDATE CASCADE,
	INDEX cs_notify_auto_index_cs_notify_cs_master_fk (id_master ASC),
	CONSTRAINT cs_notify_zone_fk FOREIGN KEY (id_zone) REFERENCES zn_zone (id_zone) ON DELETE CASCADE ON UPDATE CASCADE,
	INDEX cs_notify_auto_index_cs_notify_zone_fk (id_zone ASC),
	FAMILY "primary" (id_notify_master, id_zone, id_master)
);

CREATE TABLE cs_notify_slave (
	id_notify_slave INT NOT NULL DEFAULT unique_rowid(),
	id_notify_master INT NULL,
	id_slave INT NULL,
	CONSTRAINT cs_notify_slave_pk PRIMARY KEY (id_notify_slave ASC),
	CONSTRAINT cs_notify_slave_cs_slave_fk FOREIGN KEY (id_slave) REFERENCES cs_slave (id_slave) ON DELETE CASCADE ON UPDATE CASCADE,
	INDEX cs_notify_slave_auto_index_cs_notify_slave_cs_slave_fk (id_slave ASC),
	CONSTRAINT cs_notify_slave_cs_notify_master_fk FOREIGN KEY (id_notify_master) REFERENCES cs_notify_master (id_notify_master) ON DELETE CASCADE ON UPDATE CASCADE,
	INDEX cs_notify_slave_auto_index_cs_notify_slave_cs_notify_master_fk (id_notify_master ASC),
	FAMILY "primary" (id_notify_slave, id_notify_master, id_slave)
);

CREATE TABLE userdata (
	userdata_id INT NOT NULL DEFAULT unique_rowid(),
	user_id STRING NOT NULL,
	project_id STRING(100) NOT NULL,
	created_at TIMESTAMP NULL DEFAULT current_timestamp(),
	CONSTRAINT "primary" PRIMARY KEY (userdata_id ASC),
	UNIQUE INDEX userdata_user_id_key (user_id ASC),
	FAMILY "primary" (userdata_id, user_id, project_id, created_at)
);

CREATE TABLE zn_type (
	id_type INT NULL DEFAULT unique_rowid(),
	nm_type STRING(100) NULL,
	CONSTRAINT "primary" PRIMARY KEY (id_type ASC),
	UNIQUE INDEX zn_type_un (nm_type ASC),
	FAMILY "primary" (id_type, nm_type)
);

CREATE TABLE zn_record (
	id_record INT NOT NULL DEFAULT unique_rowid(),
	id_type INT NOT NULL,
	id_zone INT NOT NULL,
	date_record STRING(200) NULL,
	nm_record STRING(200) NULL,
	CONSTRAINT "primary" PRIMARY KEY (id_record ASC),
	CONSTRAINT fk_id_type_ref_type FOREIGN KEY (id_type) REFERENCES zn_type (id_type) ON DELETE CASCADE ON UPDATE CASCADE,
	INDEX record_auto_index_fk_id_type_ref_type (id_type ASC),
	CONSTRAINT fk_id_zone_ref_zone FOREIGN KEY (id_zone) REFERENCES zn_zone (id_zone) ON DELETE CASCADE ON UPDATE CASCADE,
	INDEX record_auto_index_fk_id_zone_ref_zone (id_zone ASC),
	FAMILY "primary" (id_record, id_type, id_zone, date_record, nm_record)
);

CREATE TABLE zn_content_serial (
	id_content_serial INT NOT NULL DEFAULT unique_rowid(),
	id_record INT NULL,
	nm_content_serial STRING NULL,
	CONSTRAINT zn_content_serial_pk PRIMARY KEY (id_content_serial ASC),
	CONSTRAINT zn_content_serial_zn_record_fk FOREIGN KEY (id_record) REFERENCES zn_record (id_record) ON DELETE CASCADE ON UPDATE CASCADE,
	INDEX zn_content_serial_auto_index_zn_content_serial_zn_record_fk (id_record ASC),
	FAMILY "primary" (id_content_serial, id_record, nm_content_serial)
);

CREATE VIEW v_content_serial (id_content_serial, id_zone, nm_zone, nm_record, id_record, nm_type, nm_content_serial) AS SELECT m1.id_content_serial, m3.id_zone, m3.nm_zone, m2.nm_record, m4.nm_type, m1.nm_content_serial FROM public.zn_content_serial AS m1 JOIN public.zn_record AS m2 ON m1.id_record = m2.id_record JOIN public.zn_zone AS m3 ON m2.id_zone = m3.id_zone JOIN public.zn_type AS m4 ON m2.id_type = m4.id_type;

CREATE TABLE zn_ttl (
	id_ttl INT NULL DEFAULT unique_rowid(),
	nm_ttl STRING(50) NULL,
	CONSTRAINT "primary" PRIMARY KEY (id_ttl ASC),
	UNIQUE INDEX zn_ttl_un (nm_ttl ASC),
	FAMILY "primary" (id_ttl, nm_ttl)
);

CREATE TABLE zn_ttldata (
	id_ttldata INT NOT NULL DEFAULT unique_rowid(),
	id_record INT NOT NULL,
	id_ttl INT NOT NULL,
	created_at TIMESTAMP NULL DEFAULT current_timestamp(),
	CONSTRAINT "primary" PRIMARY KEY (id_ttldata ASC),
	CONSTRAINT fk_id_record_ref_record FOREIGN KEY (id_record) REFERENCES zn_record (id_record) ON DELETE CASCADE ON UPDATE CASCADE,
	INDEX ttldata_auto_index_fk_id_record_ref_record (id_record ASC),
	CONSTRAINT fk_id_ttl_ref_ttl FOREIGN KEY (id_ttl) REFERENCES zn_ttl (id_ttl) ON DELETE CASCADE ON UPDATE CASCADE,
	INDEX ttldata_auto_index_fk_id_ttl_ref_ttl (id_ttl ASC),
	FAMILY "primary" (id_ttldata, id_record, id_ttl, created_at)
);

CREATE TABLE zn_content (
	id_content INT NOT NULL DEFAULT unique_rowid(),
	id_ttldata INT NULL,
	nm_content STRING NULL,
	CONSTRAINT zn_content_pk PRIMARY KEY (id_content ASC),
	CONSTRAINT zn_content_zn_ttldata_fk FOREIGN KEY (id_ttldata) REFERENCES zn_ttldata (id_ttldata) ON DELETE CASCADE ON UPDATE CASCADE,
	INDEX zn_content_auto_index_zn_content_zn_ttldata_fk (id_ttldata ASC),
	FAMILY "primary" (id_content, id_ttldata, nm_content)
);

CREATE VIEW v_contentdata (id_content, id_zone, nm_zone, id_record, nm_record, nm_type, nm_ttl, nm_content) AS SELECT m1.id_content, m5.id_zone, m5.nm_zone, m3.id_record, m3.nm_record, m6.nm_type, m4.nm_ttl, m1.nm_content FROM public.zn_content AS m1 JOIN public.zn_ttldata AS m2 ON m1.id_ttldata = m2.id_ttldata JOIN public.zn_record AS m3 ON m2.id_record = m3.id_record JOIN public.zn_ttl AS m4 ON m2.id_ttl = m4.id_ttl JOIN public.zn_type AS m6 ON m3.id_type = m6.id_type JOIN public.zn_zone AS m5 ON m3.id_zone = m5.id_zone;

CREATE VIEW v_record (id_record, id_zone, nm_zone, nm_record, date_record, nm_type) AS SELECT m1.id_record, m2.id_zone, m2.nm_zone, m1.nm_record, m1.date_record, m3.nm_type FROM public.zn_record AS m1 JOIN public.zn_zone AS m2 ON m1.id_zone = m2.id_zone JOIN public.zn_type AS m3 ON m1.id_type = m3.id_type;

CREATE VIEW v_ttldata (id_ttldata, id_ttl, id_record, id_zone, nm_zone, nm_record, nm_ttl, nm_type) AS SELECT m1.id_ttldata, m1.id_ttl, m2.id_record, m4.id_zone, m4.nm_zone, m2.nm_record, m3.nm_ttl, m5.nm_type FROM public.zn_ttldata AS m1 JOIN public.zn_record AS m2 ON m1.id_record = m2.id_record JOIN public.zn_ttl AS m3 ON m1.id_ttl = m3.id_ttl JOIN public.zn_zone AS m4 ON m2.id_zone = m4.id_zone JOIN public.zn_type AS m5 ON m2.id_type = m5.id_type;

CREATE TABLE zn_user_zone (
    id_user_zone INT NOT NULL DEFAULT unique_rowid(),
    userdata_id INT NOT NULL,
    id_zone INT NOT NULL UNIQUE,
    CONSTRAINT "primary" PRIMARY KEY (id_user_zone ASC),
    CONSTRAINT fk_userdata_id_ref FOREIGN KEY (userdata_id) REFERENCES userdata(userdata_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX user_zone_auto_index_fk_userdata_id_ref (userdata_id ASC),
    CONSTRAINT fk_id_zone_ref_zone FOREIGN KEY (id_zone) REFERENCES zn_zone (id_zone) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX user_zone_auto_index_fk_id_zone_ref_zone (id_zone ASC),
    FAMILY "primary" (id_user_zone, userdata_id,id_zone)
);

CREATE VIEW v_userzone (id_user_zone, userdata_id, id_zone, user_id, project_id, nm_zone) AS SELECT m1.id_user_zone ,
 m2.userdata_id, m3.id_zone, m2.user_id, m2.project_id, m3.nm_zone
 FROM public.zn_user_zone AS m1 JOIN public.userdata as m2 ON m1.userdata_id = m2.userdata_id JOIN public.zn_zone AS m3 ON m3.id_zone = m1.id_zone 
 ;


INSERT INTO zn_zone (id_zone, nm_zone) VALUES
	(403076482884698113, 'iank.com'),
	(403085995932844033, 'darirest.com'),
	(403086715162165249, 'lagidarirest.com'),
	(403087426993356801, '2darirest.com'),
	(403087859506577409, 'ianklagi.com'),
	(403088762180304897, 'iankwww.com'),
	(403463031250288641, 'ibnu.com'),
	(403531113784934401, 'crot.com');

INSERT INTO cs_master (id_master, nm_master, ip_master, port) VALUES
	(402152439124393985, 'master1', '0.0.0.0', '53');

INSERT INTO cs_slave (id_slave, nm_slave, ip_slave, port) VALUES
	(402152759030939649, 'slave1', '182.253.237.110', '53'),
	(402153106273501185, 'slave2', '182.253.237.111', '53');

INSERT INTO userdata (userdata_id, email, username, password, created_at) VALUES
	(402435301189451777, 'meongbego@gmail.com', 'mongkey', '$pbkdf2-sha256$29000$l1Kq1TqnNIZQCgFgzHlvjQ$AgQtiZRd6x03mwBuUzPscZJ0Xk.eOFFWAqwQPIwlV50', '2018-11-22 10:51:47.417691+00:00'),
	(415415243485904897, 'ikanisfish@gmail.com', 'ikan', '$pbkdf2-sha256$29000$zpkzRgghpPR.r9Wak5JSig$RcGRZSgYP4YGS5sEmPi4shHaxIJOXWDqqW5CpDGjHKg', '2018-11-22 10:51:47.417691+00:00'),
	(415416349489627137,'test@gmail.com', 'test', '$pbkdf2-sha256$29000$N.Zcaw3B.F/rHYOQsvaeMw$ZtJnxfyyC6O0POuV1RZdcmiv/QiNSV9A0fjnIeXm4gM', '2018-11-22 10:51:47.417691+00:00');

INSERT INTO userlogin (userlogin_id, userdata_id, username, password) VALUES
	(402435953011326977, 402435301189451777, 'mongkey', '$pbkdf2-sha256$29000$l1Kq1TqnNIZQCgFgzHlvjQ$AgQtiZRd6x03mwBuUzPscZJ0Xk.eOFFWAqwQPIwlV50'),
	(415415392702234625, 415415243485904897, 'ikan', '$pbkdf2-sha256$29000$zpkzRgghpPR.r9Wak5JSig$RcGRZSgYP4YGS5sEmPi4shHaxIJOXWDqqW5CpDGjHKg'),
	(415416448693567489, 415416349489627137, 'testtoken', '$pbkdf2-sha256$29000$N.Zcaw3B.F/rHYOQsvaeMw$ZtJnxfyyC6O0POuV1RZdcmiv/QiNSV9A0fjnIeXm4gM');

INSERT INTO zn_type (id_type, nm_type) VALUES
	(402140280385142785, 'SOA'),
	(402329131320508417, 'SRV'),
	(402386688803307521, 'A'),
	(402393625286410241, 'NS'),
	(402427533112147969, 'CNAME'),
	(402427545745850369, 'MX'),
	(402427683852124161, 'AAAA'),
	(402427759247851521, 'TXT');

INSERT INTO zn_record (id_record, id_type, id_zone, date_record, nm_record) VALUES
	(403076483056435201, 402140280385142785, 403076482884698113, '2018112500', 'iank.com'),
	(403076483429433345, 402393625286410241, 403076482884698113, '2018112500', '@'),
	(403085996111822849, 402140280385142785, 403085995932844033, '2018112501', 'darirest.com'),
	(403085996606816257, 402393625286410241, 403085995932844033, '2018112501', '@'),
	(403086715296612353, 402140280385142785, 403086715162165249, '2018112501', 'lagidarirest.com'),
	(403086715808481281, 402393625286410241, 403086715162165249, '2018112501', '@'),
	(403087427102736385, 402140280385142785, 403087426993356801, '2018112501', '2darirest.com'),
	(403087427544186881, 402393625286410241, 403087426993356801, '2018112501', '@'),
	(403087859605209089, 402140280385142785, 403087859506577409, '2018112501', 'ianklagi.com'),
	(403087859973521409, 402393625286410241, 403087859506577409, '2018112501', '@'),
	(403088762355089409, 402140280385142785, 403088762180304897, '2018112501', 'iankwww.com'),
	(403088762996129793, 402393625286410241, 403088762180304897, '2018112501', '@'),
	(403463031350493185, 402140280385142785, 403463031250288641, '2018112608', 'ibnu.com'),
	(403463031900602369, 402393625286410241, 403463031250288641, '2018112608', '@'),
	(403531114140762113, 402140280385142785, 403531113784934401, '2018112614', 'crot.com'),
	(403531114797465601, 402393625286410241, 403531113784934401, '2018112614', '@');

INSERT INTO zn_content_serial (id_content_serial, id_record, nm_content_serial) VALUES
	(403076483205136385, 403076483056435201, '10800'),
	(403076483240230913, 403076483056435201, '3600'),
	(403076483279290369, 403076483056435201, '604800'),
	(403076483317137409, 403076483056435201, '38400'),
	(403085996399591425, 403085996111822849, '10800'),
	(403085996433965057, 403085996111822849, '3600'),
	(403085996476432385, 403085996111822849, '604800'),
	(403085996519751681, 403085996111822849, '38400'),
	(403086715617640449, 403086715296612353, '10800'),
	(403086715660795905, 403086715296612353, '3600'),
	(403086715692285953, 403086715296612353, '604800'),
	(403086715723546625, 403086715296612353, '38400'),
	(403087427313762305, 403087427102736385, '10800'),
	(403087427360391169, 403087427102736385, '3600'),
	(403087427401809921, 403087427102736385, '604800'),
	(403087427437297665, 403087427102736385, '38400'),
	(403087859768688641, 403087859605209089, '10800'),
	(403087859809615873, 403087859605209089, '3600'),
	(403087859855425537, 403087859605209089, '604800'),
	(403087859894484993, 403087859605209089, '38400'),
	(403088762780778497, 403088762355089409, '10800'),
	(403088762826784769, 403088762355089409, '3600'),
	(403088762868236289, 403088762355089409, '604800'),
	(403088762911096833, 403088762355089409, '38400'),
	(403463031693574145, 403463031350493185, '10800'),
	(403463031731126273, 403463031350493185, '3600'),
	(403463031773822977, 403463031350493185, '604800'),
	(403463031814979585, 403463031350493185, '38400'),
	(403531114613866497, 403531114140762113, '10800'),
	(403531114642898945, 403531114140762113, '3600'),
	(403531114683203585, 403531114140762113, '604800'),
	(403531114723606529, 403531114140762113, '38400');

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
	(403076483094806529, 403076483056435201, 402140815780249601, '2018-11-24 17:13:00.631828+00:00'),
	(403076483503357953, 403076483429433345, 402140815780249601, '2018-11-24 17:13:00.756219+00:00'),
	(403085996217729025, 403085996111822849, 402140815780249601, '2018-11-24 18:01:23.789263+00:00'),
	(403085996669173761, 403085996606816257, 402140815780249601, '2018-11-24 18:01:23.944084+00:00'),
	(403086715393933313, 403086715296612353, 402140815780249601, '2018-11-24 18:05:03.2649+00:00'),
	(403086715870969857, 403086715808481281, 402140815780249601, '2018-11-24 18:05:03.427109+00:00'),
	(403087427167584257, 403087427102736385, 402140815780249601, '2018-11-24 18:08:40.497553+00:00'),
	(403087427610509313, 403087427544186881, 402140815780249601, '2018-11-24 18:08:40.632751+00:00'),
	(403087859657867265, 403087859605209089, 402140815780249601, '2018-11-24 18:10:52.483302+00:00'),
	(403087860012744705, 403087859973521409, 402140815780249601, '2018-11-24 18:10:52.591628+00:00'),
	(403088762515390465, 403088762355089409, 402140815780249601, '2018-11-24 18:15:27.993786+00:00'),
	(403088763055570945, 403088762996129793, 402140815780249601, '2018-11-24 18:15:28.178243+00:00'),
	(403463031434182657, 403463031350493185, 402140815780249601, '2018-11-26 01:59:05.823048+00:00'),
	(403463031962042369, 403463031900602369, 402140815780249601, '2018-11-26 01:59:05.984086+00:00'),
	(403531114345234433, 403531114140762113, 402140815780249601, '2018-11-26 07:45:23.03095+00:00'),
	(403531114852876289, 403531114797465601, 402140815780249601, '2018-11-26 07:45:23.23359+00:00');

INSERT INTO zn_content (id_content, id_ttldata, nm_content) VALUES
	(403076483136749569, 403076483094806529, 'ns1.biz.net.id.'),
	(403076483165487105, 403076483094806529, 'hostmaster.biz.net.id.'),
	(403076483579609089, 403076483503357953, 'ns1.biz.net.id.'),
	(403076483608772609, 403076483503357953, 'hostmaster.biz.net.id.'),
	(403085996278251521, 403085996217729025, 'ns1.biz.net.id.'),
	(403085996315475969, 403085996217729025, 'hostmaster.biz.net.id.'),
	(403085996778094593, 403085996669173761, 'ns1.biz.net.id.'),
	(403085996808601601, 403085996669173761, 'hostmaster.biz.net.id.'),
	(403086715543289857, 403086715393933313, 'ns1.biz.net.id.'),
	(403086715575926785, 403086715393933313, 'hostmaster.biz.net.id.'),
	(403086715939717121, 403086715870969857, 'ns1.biz.net.id.'),
	(403086715970912257, 403086715870969857, 'hostmaster.biz.net.id.'),
	(403087427229057025, 403087427167584257, 'ns1.biz.net.id.'),
	(403087427267559425, 403087427167584257, 'hostmaster.biz.net.id.'),
	(403087427714318337, 403087427610509313, 'ns1.biz.net.id.'),
	(403087427744268289, 403087427610509313, 'hostmaster.biz.net.id.'),
	(403087859709411329, 403087859657867265, 'ns1.biz.net.id.'),
	(403087859737231361, 403087859657867265, 'hostmaster.biz.net.id.'),
	(403087860056653825, 403087860012744705, 'ns1.biz.net.id.'),
	(403087860082540545, 403087860012744705, 'hostmaster.biz.net.id.'),
	(403088762610843649, 403088762515390465, 'ns1.biz.net.id.'),
	(403088762651967489, 403088762515390465, 'hostmaster.biz.net.id.'),
	(403088763129495553, 403088763055570945, 'ns1.biz.net.id.'),
	(403088763159674881, 403088763055570945, 'hostmaster.biz.net.id.'),
	(403463031524556801, 403463031434182657, 'ns1.biz.net.id.'),
	(403463031573839873, 403463031434182657, 'hostmaster.biz.net.id.'),
	(403463032037867521, 403463031962042369, 'ns1.biz.net.id.'),
	(403463032067227649, 403463031962042369, 'hostmaster.biz.net.id.'),
	(403531114479550465, 403531114345234433, 'ns1.biz.net.id.'),
	(403531114509959169, 403531114345234433, 'hostmaster.biz.net.id.'),
	(403531114919428097, 403531114852876289, 'ns1.biz.net.id.'),
	(403531114947969025, 403531114852876289, 'hostmaster.biz.net.id.');
