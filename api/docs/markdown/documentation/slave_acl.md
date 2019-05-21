# SLAVE ACL ENDPOINT


### GET SLAVE ACL
- path: /api/acl_slave
- method: GET
- response: application/json
- body: no
- roles: admin
- usage: Get all available Slave ACL

### INSERT SLAVE ACL
- path: /api/acl_slave
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Add new Slave ACL

raw:
```
{
    "insert": {
        "fields": {
            "id_acl_master": master_acl::id_acl_master,
            "id_slave": slave::id_slave
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
            "id_acl_master": "402152439123235692",
            "id_slave": "402152439124393985"
        }
    }
}
```


### SLAVE ACL WHERE

- path: /api/acl_slave
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Find slave ACL data by tag (id or name) for filtering. 

raw:
```
{
    "where": {
        "tags":{
            "id_slave": slave::id_slave,
            "id_acl_slave": slave_acl::id_acl_slave
        }
    }
}
```
- id_slave: id slave of the ACL that you're searching
- id_acl_slave: id of the ACL that you're searching

example:
```
{
   "where": {
      "tags": {
      	"id_slave": "402152439123235692"
      }
      	
   }
}
```


### SLAVE ACL REMOVE
- path: /api/acl_slave
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: remove slave 

raw:
```
{
   "remove": {
      "tags": {
      	"id_acl_slave": slave_acl::id_acl_slave
      }
      	
   }
}
```
tags:
- id_acl_slave: id of ACL slave data that will be removed

example:
```
{
   "remove": {
      "tags": {
      	"id_acl_slave": "402329670102745089"
      }
      	
   }
}
```