# CONTENT SERIAL DATA ENDPOINT
The purpose of Content Serial Data endpoint is to create, read or delete content data from an existing record.
Content Serial Data consists of several endpoints including:

### CONTENT SERIAL DATA ALL
- path: /api/content_serial
- method: get
- response: application/json
- body: no
- roles: admin
- usage: Get all content serial data and its related record id

### CONTENT SERIAL DATA ADD
- path: /api/content_serial
- method: post
- response: application/json
- body: raw
- roles: admin
- relation : [record](record.md)
- usage: Add content serial data for existing record

raw:
```
{
   "insert": {
      "fields": {
      	"id_record": record::id_record,
        "nm_content_serial": string
      }
      	
   }
}
```
fields:
- id_record: ID record which content data will be inserted
- nm_content_serial: content serial data of the record. For further information on which record type that requires serial data and its details, see [rules](RULES.md)

example:
```
{
   "insert": {
      "fields": {
      	"nm_content_serial": "38400",
        "id_record": "402339943405944833"
      }
      	
   }
}
```
See [rules](RULES_add_record.md#connecting-acnameaaatxt-record-to-ttl-data)  for other examples

### CONTENT DATA WHERE

- path: /api/content_serial
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Filter content data by one or all of its tags.

raw:
```
{
   "where": {
      "tags": {
        "id_content_serial": content::id_content
      }
   }
}
```

tags:
- id_content_serial: Filter data by its id

example:
```
{
   "where": {
      "tags": {
      	"id_content_serial": "402145755976826881"
      }
      	
   }
}
```
### CONTENT DATA REMOVE
- path: /api/content
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: remove ttl value of a record
raw:
```
{
   "remove": {
      "tags": {
      	"id_content": content::id_ttldata
      }
   }
}
```
tags:
- id_content: id of content that will be removed

example : 
```
{
   "where": {
      "tags": {
      	"id_content": "402145755976826881"
      }
      	
   }
}
```

### CONTENT SERIAL DATA VIEW
- path: /api/content_serial
- method: post
- respone: application/json
- body: raw
- roles: admin
- relation: [record](record.md), [zone](zone.md), [ttldata](ttldata.md)
- usage: View content serial data and its related data using one or all tags.

raw:
```
{
   "view": {
      "tags": {
      	"nm_zone": zone::nm_zone,
        "id_record": record::id_record,
        "id_ttldata": ttldata:id_ttldata
      }     	
   }
}
```
tags:
- nm_zone: Filter search by zone name
- id_record: Filter search by record's id
- id_ttldata: Filter search by ttldata's id

```
example:
{
    "view": {
        "tags": {
            "id_record": "425573109236203521"
        }
    }
}
```