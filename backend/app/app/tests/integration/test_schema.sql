-- This schema ported from schema.sql for PostgreSQL compatibility
CREATE TABLE "user" (
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL,
  created_at TIMESTAMP NULL
);

CREATE TABLE zone (
  id SERIAL PRIMARY KEY,
  zone TEXT NULL,
  --
  user_id SERIAL REFERENCES "user" (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE "rtype" (id SERIAL PRIMARY KEY, "rtype" TEXT NOT NULL);

CREATE TABLE ttl (id SERIAL PRIMARY KEY, ttl TEXT NOT NULL);

CREATE TABLE record (
  id SERIAL PRIMARY KEY,
  owner TEXT NULL,
  rdata TEXT NULL,
  --
  zone_id INT8 NOT NULL REFERENCES zone (id) ON DELETE CASCADE ON UPDATE CASCADE,
  rtype_id INT8 NOT NULL REFERENCES "rtype" (id) ON DELETE CASCADE ON UPDATE CASCADE,
  ttl_id SERIAL REFERENCES ttl (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Fill the default data

INSERT INTO
  "rtype" (id, "rtype")
VALUES
  (1, 'SOA'),
  (2, 'SRV'),
  (3, 'A'),
  (4, 'NS'),
  (5, 'CNAME'),
  (6, 'MX'),
  (7, 'AAAA'),
  (8, 'TXT');

INSERT INTO
  ttl (id, ttl)
VALUES
  (1, '86400'),
  (2, '43200'),
  (3, '28800'),
  (4, '14400'),
  (5, '7200'),
  (6, '3600'),
  (7, '1800'),
  (8, '900'),
  (9, '300');

-- Tell postgres we have inserted id manually.
-- Otherwise we got `duplicate key value violates unique constraint \"ttl_pkey\"\nDETAIL:  Key (id)=(1) already exists.`
SELECT setval('rtype_id_seq', (SELECT MAX(id) from "rtype"));
SELECT setval('ttl_id_seq', (SELECT MAX(id) from "ttl"));
