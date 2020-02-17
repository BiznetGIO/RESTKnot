-- This schema ported from schema.sql for PostgreSQL compatibility
CREATE TABLE "user" (
	id SERIAL UNIQUE,
	email VARCHAR NOT NULL,
	created_at TIMESTAMP NULL
);

CREATE TABLE "type" (
        id SERIAL UNIQUE,
	"type" VARCHAR NULL
);


CREATE TABLE ttl (
        id SERIAL UNIQUE,
	ttl VARCHAR NULL
);

CREATE TABLE zone (
        id SERIAL UNIQUE,
	zone VARCHAR NULL,
        is_committed BOOL NULL,
        user_id SERIAL REFERENCES "user" (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE record (
        id SERIAL UNIQUE,
	owner VARCHAR NULL,
        zone_id INT8 NOT NULL REFERENCES zone (id) ON DELETE CASCADE ON UPDATE CASCADE,
        type_id INT8 NOT NULL REFERENCES "type" (id) ON DELETE CASCADE ON UPDATE CASCADE,
        ttl_id SERIAL REFERENCES ttl (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE rdata (
        id SERIAL UNIQUE,
        rdata VARCHAR NULL,
        record_id SERIAL REFERENCES record (id) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO "type" (id, "type") VALUES
	(1, 'SOA'),
	(2, 'SRV'),
	(3, 'A'),
	(4, 'NS'),
	(5, 'CNAME'),
	(6, 'MX'),
	(7, 'AAAA'),
	(8, 'TXT');

INSERT INTO ttl (id, ttl) VALUES
	(1, '86400'),
	(2, '43200'),
	(3, '28800'),
	(4, '14400'),
	(5, '7200'),
	(6, '3600'),
	(7, '1800'),
	(8, '900'),
	(9, '300');
