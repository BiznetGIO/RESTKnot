# TTL ENDPOINT
TTL consists of several endpoints including:

### TTL ALL
- path: /api/ttl
- method: get
- response: application/json
- body: no
- roles: admin
- usage: Get all available TTL values

### TTL ADD
- path: /api/ttl
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Add new TTL value

raw:
```
{
    "insert": {
        "fields": {
            "nm_ttl": string
        }
    }
}
```
fields:
- nm_ttl : TTL value that's going to be inserted

example:
```
{
    "insert": {
        "fields": {
            "nm_ttl": "300"
        }
    }
}
```
See [rules](RULES_add_record.md) for other examples

### TTL WHERE

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
        "tags":{
            "id_ttl": ttl::id_ttl,
            "nm_ttl": string
        }
    }
}
```
- id_ttl: id of the ttl that you're searching
- nm_ttl: name of the ttl that you're searching

example:
```
{
   "where": {
      "tags": {
      	"nm_ttl": "300"
      }
      	
   }
}
```


### TTL REMOVE
- path: /api/ttl
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: remove ttl values

raw:
```
{
   "remove": {
      "tags": {
      	"id_ttl": ttl::id_ttl
      }
      	
   }
}
```
tags:
- id_ttl: id of ttl value that will be removed

example:
```
{
   "remove": {
      "tags": {
      	"id_ttl": "402329670102745089"
      }
      	
   }
}
```