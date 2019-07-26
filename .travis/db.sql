CREATE SEQUENCE mytable_id_seq;

CREATE OR REPLACE FUNCTION pseudo_encrypt(VALUE bigint) returns bigint AS $$
DECLARE
l1 bigint;
l2 bigint;
r1 bigint;
r2 bigint;
i int:=0;
BEGIN
    l1:= (VALUE >> 32) & 4294967295::bigint;
    r1:= VALUE & 4294967295;
    WHILE i < 3 LOOP
        l2 := r1;
        r2 := l1 # ((((1366.0 * r1 + 150889) % 714025) / 714025.0) * 32767*32767)::int;
        l1 := l2;
        r1 := r2;
        i := i + 1;
    END LOOP;
RETURN ((l1::bigint << 32) + r1);
END;
$$ LANGUAGE plpgsql strict immutable;


CREATE TABLE cs_master (
	id_master bigint not null default pseudo_encrypt(nextval('mytable_id_seq')),
	nm_master VARCHAR(200) NULL,
	ip_master VARCHAR(200) NULL,
	port VARCHAR(200) NULL DEFAULT '53',
	nm_config VARCHAR NULL,
	CONSTRAINT "master_pk" PRIMARY KEY (id_master),
	UNIQUE (nm_master)
	);

CREATE TABLE cs_slave_node (
	id_cs_slave_node bigint NOT NULL default pseudo_encrypt(nextval('mytable_id_seq')),
	id_master bigint NULL,
	nm_slave_node VARCHAR NULL,
	ip_slave_node VARCHAR NULL,
	port_slave_node VARCHAR NULL,
	CONSTRAINT "slave_pk" PRIMARY KEY (id_cs_slave_node),
	UNIQUE (id_cs_slave_node)
	);

CREATE INDEX cs_slave_node_auto_index_cs_id_master_fk ON cs_slave_node(id_master ASC);

CREATE TABLE userdata (
	userdata_id bigint NOT NULL default pseudo_encrypt(nextval('mytable_id_seq')),
	user_id VARCHAR NOT NULL,
	project_id VARCHAR(100) NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT "userdata_pk" PRIMARY KEY (userdata_id),
	UNIQUE(user_id)
);

CREATE TABLE zn_type (
	id_type bigint NOT NULL default pseudo_encrypt(nextval('mytable_id_seq')),
	nm_type VARCHAR(100) NULL,
	CONSTRAINT "type_pk" PRIMARY KEY (id_type),
	UNIQUE (nm_type)
);

CREATE TABLE zn_zone (
	id_zone bigint not null default pseudo_encrypt(nextval('mytable_id_seq')),
	nm_zone VARCHAR(200) NULL,
	state INT NULL DEFAULT 0,
	counter INT NOT NULL DEFAULT 0,
	CONSTRAINT "zone_pk" PRIMARY KEY(id_zone),
	UNIQUE (nm_zone)
);


CREATE TABLE zn_record (
	id_record bigint NOT NULL default pseudo_encrypt(nextval('mytable_id_seq')),
	id_type bigint NULL,
	id_zone bigint NULL,
	date_record VARCHAR(200) NULL,
	nm_record VARCHAR(200) NULL,
	state bigint NULL DEFAULT 0,
	CONSTRAINT "record_pk" PRIMARY KEY (id_record)
);

CREATE INDEX record_auto_index_fk_id_type_ref_type ON zn_record(id_type ASC);
CREATE INDEX record_auto_index_fk_id_zone_ref_zone ON zn_record(id_zone ASC);

CREATE TABLE zn_content_serial (
	id_content_serial bigint NOT NULL default pseudo_encrypt(nextval('mytable_id_seq')),
	id_record bigint NULL,
	nm_content_serial VARCHAR NULL,
	CONSTRAINT zn_content_serial_pk PRIMARY KEY (id_content_serial)
);

CREATE INDEX zn_content_serial_auto_index_zn_content_serial_zn_record_fk ON zn_content_serial(id_record ASC);

CREATE VIEW v_content_serial (id_content_serial, id_zone, nm_zone, nm_record, id_record, nm_type, nm_content_serial) AS SELECT m1.id_content_serial, m3.id_zone, m3.nm_zone, m2.nm_record, m2.id_record, m4.nm_type, m1.nm_content_serial FROM public.zn_content_serial AS m1 JOIN public.zn_record AS m2 ON m1.id_record = m2.id_record JOIN public.zn_zone AS m3 ON m2.id_zone = m3.id_zone JOIN public.zn_type AS m4 ON m2.id_type = m4.id_type;

CREATE TABLE zn_ttl (
	id_ttl bigint NOT NULL default pseudo_encrypt(nextval('mytable_id_seq')),
	nm_ttl VARCHAR(50) NULL,
	CONSTRAINT zn_ttl_pk PRIMARY KEY (id_ttl)
);

CREATE INDEX zn_ttl_un ON zn_ttl(nm_ttl ASC);

CREATE TABLE zn_ttldata (
	id_ttldata bigint NOT NULL default pseudo_encrypt(nextval('mytable_id_seq')),
	id_record bigint NOT NULL,
	id_ttl bigint NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT zn_ttl_data_pk PRIMARY KEY (id_ttldata)
	);

CREATE INDEX ttldata_auto_index_fk_id_record_ref_record ON zn_ttldata(id_record ASC);
CREATE INDEX ttldata_auto_index_fk_id_ttl_ref_ttl ON zn_ttldata(id_ttl ASC);

CREATE TABLE zn_content (
	id_content bigint NOT NULL default pseudo_encrypt(nextval('mytable_id_seq')),
	id_ttldata bigint NULL,
	nm_content VARCHAR NULL,
	CONSTRAINT zn_content_pk PRIMARY KEY (id_content)
);

CREATE INDEX zn_content_auto_index_zn_content_zn_ttldata_fk ON zn_content(id_ttldata ASC);
CREATE VIEW v_contentdata (id_content, id_zone, nm_zone, id_record, nm_record, nm_type, nm_ttl, nm_content) AS SELECT m1.id_content, m5.id_zone, m5.nm_zone, m3.id_record, m3.nm_record, m6.nm_type, m4.nm_ttl, m1.nm_content FROM public.zn_content AS m1 JOIN public.zn_ttldata AS m2 ON m1.id_ttldata = m2.id_ttldata JOIN public.zn_record AS m3 ON m2.id_record = m3.id_record JOIN public.zn_ttl AS m4 ON m2.id_ttl = m4.id_ttl JOIN public.zn_type AS m6 ON m3.id_type = m6.id_type JOIN public.zn_zone AS m5 ON m3.id_zone = m5.id_zone;

CREATE VIEW v_cs_slave_node (id_cs_slave_node, id_master, nm_slave_node, ip_slave_node, port_slave_node, ip_master, nm_config, master_port, nm_master) AS SELECT m1.id_cs_slave_node, m1.id_master, m1.nm_slave_node, m1.ip_slave_node, m1.port_slave_node, m2.ip_master, m2.nm_config, m2.port AS master_port, m2.nm_master FROM public.cs_slave_node AS m1 JOIN public.cs_master AS m2 ON m1.id_master = m2.id_master;

CREATE VIEW v_record (id_record, id_zone, nm_zone, nm_record, date_record, nm_type, state, counter) AS SELECT m1.id_record, m2.id_zone, m2.nm_zone, m1.nm_record, m1.date_record, m3.nm_type, m1.state, m2.counter FROM public.zn_record AS m1 JOIN public.zn_zone AS m2 ON m1.id_zone = m2.id_zone JOIN public.zn_type AS m3 ON m1.id_type = m3.id_type;

CREATE VIEW v_ttldata (id_ttldata, id_ttl, id_record, id_zone, nm_zone, nm_record, nm_ttl, nm_type) AS SELECT m1.id_ttldata, m1.id_ttl, m2.id_record, m4.id_zone, m4.nm_zone, m2.nm_record, m3.nm_ttl, m5.nm_type FROM public.zn_ttldata AS m1 JOIN public.zn_record AS m2 ON m1.id_record = m2.id_record JOIN public.zn_ttl AS m3 ON m1.id_ttl = m3.id_ttl JOIN public.zn_zone AS m4 ON m2.id_zone = m4.id_zone JOIN public.zn_type AS m5 ON m2.id_type = m5.id_type;

CREATE TABLE zn_user_zone (
	id_user_zone bigint NOT NULL default pseudo_encrypt(nextval('mytable_id_seq')),
	userdata_id bigint NOT NULL,
	id_zone bigint NOT NULL,
	CONSTRAINT zn_user_zone_pk PRIMARY KEY (id_user_zone)
	);

CREATE UNIQUE INDEX zn_user_zone_id_zone_key ON zn_user_zone(id_zone ASC);
CREATE INDEX user_zone_auto_index_fk_userdata_id_ref ON zn_user_zone (userdata_id ASC);
CREATE INDEX user_zone_auto_index_fk_id_zone_ref_zone ON zn_user_zone (id_zone ASC);
CREATE VIEW v_userzone (id_user_zone, userdata_id, id_zone, user_id, project_id, nm_zone, state) AS SELECT m1.id_user_zone, m2.userdata_id, m3.id_zone, m2.user_id, m2.project_id, m3.nm_zone, m3.state FROM public.zn_user_zone AS m1 JOIN public.userdata AS m2 ON m1.userdata_id = m2.userdata_id JOIN public.zn_zone AS m3 ON m3.id_zone = m1.id_zone;

ALTER TABLE cs_slave_node ADD CONSTRAINT cs_id_master_fk FOREIGN KEY (id_master) REFERENCES cs_master (id_master) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE zn_record ADD CONSTRAINT fk_id_type_ref_type FOREIGN KEY (id_type) REFERENCES zn_type (id_type) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE zn_record ADD CONSTRAINT fk_id_zone_ref_zone FOREIGN KEY (id_zone) REFERENCES zn_zone (id_zone) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE zn_content_serial ADD CONSTRAINT zn_content_serial_zn_record_fk FOREIGN KEY (id_record) REFERENCES zn_record (id_record) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE zn_ttldata ADD CONSTRAINT fk_id_record_ref_record FOREIGN KEY (id_record) REFERENCES zn_record (id_record) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE zn_ttldata ADD CONSTRAINT fk_id_ttl_ref_ttl FOREIGN KEY (id_ttl) REFERENCES zn_ttl (id_ttl) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE zn_content ADD CONSTRAINT zn_content_zn_ttldata_fk FOREIGN KEY (id_ttldata) REFERENCES zn_ttldata (id_ttldata) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE zn_user_zone ADD CONSTRAINT fk_id_zone_ref_zone FOREIGN KEY (id_zone) REFERENCES zn_zone (id_zone) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE zn_user_zone ADD CONSTRAINT fk_userdata_id_ref FOREIGN KEY (userdata_id) REFERENCES userdata (userdata_id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE cs_slave_node VALIDATE CONSTRAINT cs_id_master_fk;
ALTER TABLE zn_record VALIDATE CONSTRAINT fk_id_type_ref_type;
ALTER TABLE zn_record VALIDATE CONSTRAINT fk_id_zone_ref_zone;
ALTER TABLE zn_content_serial VALIDATE CONSTRAINT zn_content_serial_zn_record_fk;
ALTER TABLE zn_ttldata VALIDATE CONSTRAINT fk_id_record_ref_record;
ALTER TABLE zn_ttldata VALIDATE CONSTRAINT fk_id_ttl_ref_ttl;
ALTER TABLE zn_content VALIDATE CONSTRAINT zn_content_zn_ttldata_fk;
ALTER TABLE zn_user_zone VALIDATE CONSTRAINT fk_id_zone_ref_zone;
ALTER TABLE zn_user_zone VALIDATE CONSTRAINT fk_userdata_id_ref;

INSERT INTO cs_master (id_master, nm_master, ip_master, port, nm_config) VALUES
	(402152439124393985, 'cmg01z00knms001', '127.0.0.1', '6967', 'cmg'),
	(461914324975517697, 'jkt01z00knms001', '127.0.0.1', '6967', 'jkt');

INSERT INTO cs_slave_node (id_cs_slave_node, id_master, nm_slave_node, ip_slave_node, port_slave_node) VALUES
	(461938251232804865, 402152439124393985, 'cmg01z00knsl001', '127.0.0.1', '6967'),
	(461938251266490369, 461914324975517697, 'jkt01z00knsl001', '127.0.0.1', '6967');

INSERT INTO zn_type (id_type, nm_type) VALUES
	(402140280385142785, 'SOA'),
	(402329131320508417, 'SRV'),
	(402386688803307521, 'A'),
	(402393625286410241, 'NS'),
	(402427533112147969, 'CNAME'),
	(402427545745850369, 'MX'),
	(402427683852124161, 'AAAA'),
	(402427759247851521, 'TXT');

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
