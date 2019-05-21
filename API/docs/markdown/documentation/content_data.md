# CONTENT DATA ENDPOINT
The purpose of Content Data endpoint is to create, read or delete content data from an existing record.
Content Data consists of several endpoints including:

### CONTENT DATA ALL
- path: /api/content
- method: get
- response: application/json
- body: no
- roles: admin
- usage: Get all content data and its related ttldata id

### CONTENT DATA ADD
- path: /api/content
- method: post
- response: application/json
- body: raw
- roles: admin
- relation : [record](record.md),[ttl](ttl.md)
- usage: Add content data for existing record

raw:
```
{
   "insert": {
      "fields": {
      	"id_ttldata": ttldata::id_ttldata,
        "nm_content": string
      }
      	
   }
}
```
fields:
- id_ttldata: ID ttldata of the corresponding record which content data will be inserted
- nm_content: content data of the record. For further information of content data for various record see [rules](RULES.md)

example:
```
{
   "insert": {
      "fields": {
      	"id_ttldata": "420627361432338433",
        "nm_content": "1.1.1.1"
      }
      	
   }
}
```
See [rules](RULES_add_record.md#connecting-acnameaaatxt-record-to-ttl-data)  for other examples

### CONTENT DATA WHERE

- path: /api/content
- method: post
- response: application/json
- body: raw
- roles: admin
- relation: [record](record.md),[ttldata](ttldata.md)
- usage: Filter content data by one or all of its tags.

raw:
```
{
   "where": {
      "tags": {
        "id_content": content::id_content,
        "id_record": record::id_record,
      	"id_ttldata": ttldata::id_ttldata
      }
   }
}
```

tags:
- id_ttldata: Filter data by its ttldata id
- id_content: Filter data by its content id
- id_record: Filter data by its record id

example:
```
{
   "where": {
      "tags": {
      	"id_ttldata": "402145755976826881"
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

### CONTENT DATA VIEW
- path: /api/content
- method: post
- respone: application/json
- body: raw
- roles: admin
- relation: [record](record.md), [zone](zone.md), [ttldata](ttldata.md)
- usage: View content data and its related data using one or all tags.

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