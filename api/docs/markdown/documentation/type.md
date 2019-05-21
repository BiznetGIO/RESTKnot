# TYPE ENDPOINT
Type consists of several endpoints including:

### TYPE ALL
- path: /api/type
- method: get
- response: application/json
- body: no
- roles: admin
- usage: Get all data on record type

### TYPE ADD
- path: /api/type
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Add new record type value

raw:
```
{
   "insert": {
      "fields": {
      	"nm_type": string
      }
   }
}
```
fields:
- nm_type: Record type that's going to be inserted

example:
```
{
   "insert": {
      "fields": {
      	"nm_type": "A"
      }
   }
}
```
See [rules](RULES_add_record.md) for other examples

### TYPE WHERE

- path: /api/type
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Find type data by tag (id or name) for filtering. 

raw:
```
{
   "where": {
      "tags": {
      	"id_type": type::id_type,
         "nm_type": type::nm_type
      }
   }
}
```

tags:
- id_type: id of the record that you're searching
- nm_type: name of the record data that you're searching

example:
```
{
   "where": {
      "tags": {
      	"nm_type": "SOA"
      }
      	
   }
}
```
### TYPE REMOVE
- path: /api/type
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: remove record type
raw:
```
{
   "remove": {
      "tags": {
      	"id_type": type::id_type
      }
   }
}
```
tags:
- id_type: id of record type that will be removed

example:
```
{
   "remove": {
      "tags": {
      	"id_type": "402329670102745089"
      }
   }
}
```









