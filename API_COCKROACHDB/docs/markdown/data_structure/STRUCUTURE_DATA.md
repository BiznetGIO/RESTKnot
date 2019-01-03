## TYPE
|  Field  |    Type     | Null |    Default     |         Indices          |
|---------|-------------|------|----------------|--------------------------|
| id_type | INT         | true | unique_rowid() | {"primary","zn_type_un"} |
| nm_type | STRING(100) | true | NULL           | {"zn_type_un"}           |

## TTL
| Field  |    Type    | Null |    Default     |         Indices         |
|--------|------------|------|----------------|-------------------------|
| id_ttl | INT        | true | unique_rowid() | {"primary","zn_ttl_un"} |
| nm_ttl | STRING(50) | true | NULL           | {"zn_ttl_un"}           |

## ZONE
|  Field  |    Type     | Null |    Default     |             Indices              |
|---------|-------------|------|----------------|----------------------------------|
| id_zone | INT         | true | unique_rowid() | {"primary","zone_zone_name_key"} |
| nm_zone | STRING(200) | true | NULL           | {"zone_zone_name_key"}           |


## RECORD
|    Field    |    Type     | Null  |    Default     |                                           Indices                                           |
|-------------|-------------|-------|----------------|---------------------------------------------------------------------------------------------|
| id_record   | INT         | false | unique_rowid() | {"primary","record_auto_index_fk_id_type_ref_type","record_auto_index_fk_id_zone_ref_zone"} |
| id_type     | INT         | false | NULL           | {"record_auto_index_fk_id_type_ref_type"}                                                   |
| id_zone     | INT         | false | NULL           | {"record_auto_index_fk_id_zone_ref_zone"}                                                   |
| date_record | STRING(200) | true  | NULL           | {}                                                                                          |
| nm_record   | STRING(200) | true  | NULL           | {}                                                                                          |

## TTL DATA
|   Field    |   Type    | Null  |       Default       |                                             Indices                                             |
|------------|-----------|-------|---------------------|-------------------------------------------------------------------------------------------------|
| id_ttldata | INT       | false | unique_rowid()      | {"primary","ttldata_auto_index_fk_id_record_ref_record","ttldata_auto_index_fk_id_ttl_ref_ttl"} |
| id_record  | INT       | false | NULL                | {"ttldata_auto_index_fk_id_record_ref_record"}                                                  |
| id_ttl     | INT       | false | NULL                | {"ttldata_auto_index_fk_id_ttl_ref_ttl"}                                                        |
| created_at | TIMESTAMP | true  | current_timestamp() | {}                                                                                              |

## CONTENT
|   Field    |  Type  | Null  |    Default     |                              Indices                               |
|------------|--------|-------|----------------|--------------------------------------------------------------------|
| id_content | INT    | false | unique_rowid() | {"zn_content_pk","zn_content_auto_index_zn_content_zn_ttldata_fk"} |
| id_ttldata | INT    | true  | NULL           | {"zn_content_auto_index_zn_content_zn_ttldata_fk"}                 |
| nm_content | STRING | true  | NULL           | {}                                                                 |

## CONTENT SERIAL
|       Field       |  Type  | Null  |    Default     |                                        Indices                                         |
|-------------------|--------|-------|----------------|----------------------------------------------------------------------------------------|
| id_content_serial | INT    | false | unique_rowid() | {"zn_content_serial_pk","zn_content_serial_auto_index_zn_content_serial_zn_record_fk"} |
| id_record         | INT    | true  | NULL           | {"zn_content_serial_auto_index_zn_content_serial_zn_record_fk"}                        |
| nm_content_serial | STRING | true  | NULL           | {}                                                                                     |