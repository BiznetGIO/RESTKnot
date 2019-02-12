# RECORD ENDPOINT
Record consists of several endpoints including:

### RECORD ALL
- path: /api/record
- method: get
- response: application/json
- body: no
- roles: user
- usage: Get all available record data

### RECORD ADD
- path: /api/ttl
- method: post
- response: application/json
- body: raw
- roles: user
- relation: [zone](zone.md), [ttl](ttl.md),[type](type.md)
- usage: Add new record for an existing zone

raw:
```
{
    "insert": {
        "fields": {
            "nm_record": string,
            "id_zone": zone::id_zone,
            "id_type": type::id_type,
            "date_record": str
        }
    }
}
```
fields:
- nm_record: Name of the record that's going to be inserted
- id_zone: ID of corresponding zone for this record
- id_type: ID of the type of this record
- date_record: The date when this record is added, format (YYYYMMDDHH)

example:
```
{
   "insert": {
      "fields": {
      	"nm_record":"www",
        "date_record":"2018070410",
        "id_zone":"420622599268663297",
        "id_type":"402386688803307521"
      }
      	
   }
}
```
See [rules](RULES_add_record.md) for other examples

### RECORD WHERE

- path: /api/record
- method: post
- response: application/json
- body: raw
- roles: user
- relation: [zone](zone.md)
- usage: Find type data by one or combination of tags for filtering. 

raw:
```
{
    "where": {
        "tags":{
            "id_record": record::id_record,
            "nm_record": record::nm_record,
            "id_zone": zone::id_zone
        }
    }
}
```
- id_record: Filter data by record's id
- nm_record: Filter data by record's name
- id_zone: Filter data by zone's id
example:
```
{
   "where": {
      "tags": {
      	"id_zone": "425573109236203521"
      }
      	
   }
}
```


### RECORD REMOVE
- path: /api/record
- method: post
- response: application/json
- body: raw
- roles: user
- usage: remove record data

raw:
```
{
   "remove": {
      "tags": {
      	"id_record": record::id_record
      }
      	
   }
}
```
tags:
- id_record: id of record data that will be removed

example:
```
{
   "remove": {
      "tags": {
      	"id_record": "402329670102745089"
      }
      	
   }
}
```

### RECORD VIEW
- path: /api/record
- method: post
- response: application/json
- body: raw
- roles: user
- usage: View record and its related data

raw:
```
{
   "remove": {
      "tags": {
      	"id_record": record::id_record
      }
      	
   }
}
```
tags:
- id_record: id of record data that will be removed

raw
```
{
   "view": {
      "tags": {
      	"id_record": record::id_record
      }
      	
   }
}
```

example:
```
{
   "view": {
      "tags": {
      	"id_record": "402329670102745089"
      }
      	
   }
}
```
