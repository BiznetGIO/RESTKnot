# ZONE ENDPOINT
Zone consists of several endpoints including:

### TYPE ALL
- path: /api/zone
- method: get
- response: application/json
- body: no
- roles: admin
- usage: Get all zone data

### ZONE ADD
- path: /api/zone
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Add new zone

raw:
```
{
   "insert": {
      "fields": {
      	"nm_zone": string
      }
   }
}
```
fields:
- nm_zone: Name of the zone that would be inserted

example:
```
{
   "insert": {
      "fields": {
      	"nm_zone": "tylerberkarya.com"
      }
   }
}
```
See [rules](RULES_add_domain.md) for other examples

### ZONE WHERE

- path: /api/zone
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Find zone data by tag (id or name) for filtering. 

raw:
```
{
   "where": {
      "tags": {
      	"id_zone": zone::id_zone,
        "nm_zone": zone::nm_zone
      }
   }
}
```

tags:
- id_zone: id of the zone that you're searching
- nm_zone: name of the zone data that you're searching

example:
```
{
   "where": {
      "tags": {
      	"nm_type": "kucing.com"
      }
      	
   }
}
```
### ZONE REMOVE
- path: /api/zone
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: remove zone

raw:
```
{
   "remove": {
      "tags": {
      	"id_zone": zone::id_zone
      }
   }
}
```
tags:
- id_zone: id of zone that will be removed

example:
```
{
   "remove": {
      "tags": {
      	"id_zone": "402329670102745089"
      }
   }
}
```









