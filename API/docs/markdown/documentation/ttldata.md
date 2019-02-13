# TTLDATA ENDPOINT
The purpose of TTLData endpoint is to link a record and its ttl value.
TTLData consists of several endpoints including:

### TTLDATA ALL
- path: /api/ttldata
- method: get
- response: application/json
- body: no
- roles: admin
- usage: Get all ttl values and its related record id

### TTLDATA ADD
- path: /api/ttldata
- method: post
- response: application/json
- body: raw
- roles: admin
- relation: [record](record.md), [ttl](ttl.md)
- usage: Add ttl value for existing record

raw:
```
{
   "insert": {
      "fields": {
        "id_record": record::id_record,
        "id_ttl": ttl::id_ttl
      }
      	
   }
}
```
fields:
- id_record: ID record that will be processed
- id_ttl: ID ttl that will be inserted to record

example:
```
{
   "insert": {
      "fields": {
        "id_record": "420627223526047745",
        "id_ttl": "402427994557939713"
      }
      	
   }
}
```
See [rules](RULES_add_record.md#connecting-acnameaaatxt-record-to-ttl-data) for steps before adding ttldata

### TYPE WHERE

- path: /api/type
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Find ttldata by its id for filtering. 

raw:
```
{
   "where": {
      "tags": {
      	"id_ttldata": ttldata::id_ttldata
      }
   }
}
```

tags:
- id_ttldata: id of the ttldata that you're searching

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
### TTLDATA REMOVE
- path: /api/ttldata
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
      	"id_ttldata": ttldata:id_ttldata
      }
   }
}
```
tags:
- id_ttldata: id of ttldata that will be removed

example : 
```
{
   "where": {
      "tags": {
      	"id_ttldata": "402145755976826881"
      }
      	
   }
}
```
### TTLDATA VIEW
- path: /api/ttldata
- method: post
- respone: application/json
- body: raw
- roles: admin
- relation: [record](record.md), [zone](zone.md)
- usage: View ttldata values and its related data using one or both tags.

raw:
```
{
   "view": {
      "tags": {
      	"nm_zone": zone::nm_zone,
        "id_record": record::id_record
      }     	
   }
}
```
tags:
- nm_zone: Filter search by zone name
- id_record: Filter search by record's id

example:
```
{
    "view": {
        "tags": {
            "id_record": "425573109236203521"
        }
    }
}
```