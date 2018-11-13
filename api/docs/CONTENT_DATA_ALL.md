## CONTENT_DATA_ALL
### CONTENT_DATA_ADD
-------------------
#### POST
| NO | FIELDS | FIELD_VALUE | TAGS       | TAGS_VALUE |
|----|--------|-------------|------------|------------|
| 1  |        |             | content_id | STRING     |
### CONTENT_DATA_WHERE
---------------------
#### POST

| NO | FIELDS | FIELD_VALUE | TAGS            | TAGS_VALUE |
|----|--------|-------------|-----------------|------------|
| 1  |        |             | content_data_id | INT        |

### CONTENT_DATA_REMOVE
----------------------
#### POST
| NO | FIELDS | FIELD_VALUE | TAGS            | TAGS_VALUE |
|----|--------|-------------|-----------------|------------|
| 1  |        |             | content_data_id | INT        |

### CONF_INSERT_COMMAND
----------------
#### POST
| NO | FIELDS | FIELD_VALUE | TAGS      | TAGS_VALUE |
|----|--------|-------------|-----------|------------|
| 1  |        |             | domain_id | GET        |

### ZONE_READ_COMMAND
-------------------
#### POST
| NO | FIELDS | FIELD_VALUE | TAGS      | TAGS_VALUE |
|----|--------|-------------|-----------|------------|
| 1  |        |             | domain_id | GET        |

### ZONE_BEGIN_COMMAND
-------------------
#### POST
| NO | FIELDS | FIELD_VALUE | TAGS      | TAGS_VALUE |
|----|--------|-------------|-----------|------------|
| 1  |        |             | domain_id | GET        |

### ZONE_SOA_INSERT_COMMAND
------------------------------
#### POST
| NO | FIELDS | FIELD_VALUE | TAGS        | TAGS_VALUE |
|----|--------|-------------|-------------|------------|
| 1  |        |             | zone_id     | GET        |
| 2  |        |             | ttl_data_id | GET        |


### ZONE_COMMIT_COMMAND
-----------------------
#### POST

| NO | FIELDS | FIELD_VALUE | TAGS      | TAGS_VALUE |
|----|--------|-------------|-----------|------------|
| 1  |        |             | domain_id | GET        |
