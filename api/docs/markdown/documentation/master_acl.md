# MASTER ACL ENDPOINT


### GET MASTER ACL
- path: /api/acl_master
- method: GET
- response: application/json
- body: no
- roles: admin
- usage: Get all available Master ACL

### INSERT MASTER ACL
- path: /api/acl_master
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Add new Master ACL

raw:
```
{
    "insert": {
        "fields": {
            "id_zone": zone::id_zone,
            "id_master": master::id_master
        }
    }
}
```
fields:


example:
```
{
    "insert": {
        "fields": {
            "id_zone": "402152439123235692",
            "id_master": "402152439124393985"
        }
    }
}
```


### MASTER WHERE

- path: /api/acl_master
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Find master ACL data by tag (id or name) for filtering. 

raw:
```
{
    "where": {
        "tags":{
            "id_master": master::id_master,
            "id_acl_master": master_acl::id_acl_master,
            "id_zone": zone::id_zone

        }
    }
}
```
- id_master: id master of the ACL that you're searching
- id_acl_master: id of the ACL that you're searching
- id_zone: id zone of the ACL that you're searching

example:
```
{
   "where": {
      "tags": {
      	"id_zone": "402152439123235692"
      }
      	
   }
}
```


### MASTER REMOVE
- path: /api/acl_master
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: remove master 

raw:
```
{
   "remove": {
      "tags": {
      	"id_acl_master": master_acl::id_acl_master
      }
      	
   }
}
```
tags:
- id_acl_master: id of ACL master data that will be removed

example:
```
{
   "remove": {
      "tags": {
      	"id_acl_master": "402329670102745089"
      }
      	
   }
}
```