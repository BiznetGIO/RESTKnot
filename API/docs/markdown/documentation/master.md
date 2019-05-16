# MASTER ENDPOINT
Consists of IP, port and name of Master Devices

### GET MASTER 
- path: /api/master
- method: GET
- response: application/json
- body: no
- roles: admin
- usage: Get all available Master Devices

### INSERT MASTER
- path: /api/master
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Add new Master Device

raw:
```
{
    "insert": {
        "fields": {
            "nm_master": string,
            "ip_master": string,
            "port"     : string
        }
    }
}
```
fields:
- nm_master : Master device's name
- ip_master : Master's IP address
- port      : Port used by Master device

example:
```
{
    "insert": {
        "fields": {
            "nm_master": "yoda",
            "ip_master": "127.0.0.1",
            "port"     : "50"
        }
    }
}
```


### MASTER WHERE

- path: /api/master
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
            "id_master": master::id_master,
            "nm_master": master::nm_master,
            "ip_master": master::ip_master

        }
    }
}
```
- id_master: id of the master that you're searching
- nm_master: name of the master that you're searching
- ip_master: ip address of the master that you're searching

example:
```
{
   "where": {
      "tags": {
      	"nm_master": "mas_master"
      }
      	
   }
}
```


### MASTER REMOVE
- path: /api/master
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
      	"id_master": ttl::id_master
      }
      	
   }
}
```
tags:
- id_master: id of master data that will be removed

example:
```
{
   "remove": {
      "tags": {
      	"id_master": "402329670102745089"
      }
      	
   }
}
```