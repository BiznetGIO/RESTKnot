CREATE TABLE "user" (
  id INT8 NOT NULL PRIMARY KEY DEFAULT unique_rowid(),
  email STRING NOT NULL,
  created_at TIMESTAMP NULL DEFAULT current_timestamp() :: :TIMESTAMP
);

CREATE TABLE zone (
  id INT8 NOT NULL PRIMARY KEY DEFAULT unique_rowid(),
  user_id INT8 NOT NULL REFERENCES "user" (id) ON DELETE CASCADE ON UPDATE CASCADE,
  --
  zone STRING NULL,
);

CREATE TABLE "type" (
  id INT8 NOT NULL PRIMARY KEY DEFAULT unique_rowid(),
  "type" STRING NULL
);

CREATE TABLE ttl (
  id INT NOT NULL PRIMARY KEY DEFAULT unique_rowid(),
  ttl STRING NULL
);

CREATE TABLE record (
  id INT8 NOT NULL PRIMARY KEY DEFAULT unique_rowid(),
  zone_id INT8 NOT NULL REFERENCES zone (id) ON DELETE CASCADE ON UPDATE CASCADE,
  type_id INT8 NOT NULL REFERENCES "type" (id) ON DELETE CASCADE ON UPDATE CASCADE,
  ttl_id INT8 NOT NULL REFERENCES ttl (id) ON DELETE CASCADE ON UPDATE CASCADE,
  --
  owner STRING NULL,
  rdata STRING NULL
);


-- Fill the default data

INSERT INTO
  "type" (id, "type")
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
