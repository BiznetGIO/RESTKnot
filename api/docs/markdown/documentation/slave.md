# SLAVE ENDPOINT
Consists of IP, port and name of slave Devices

### GET SLAVE 
- path: /api/slave
- method: GET
- response: application/json
- body: no
- roles: admin
- usage: Get all available slave Devices

### INSERT SLAVE
- path: /api/slave
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Add new slave Device

raw:
```
{
    "insert": {
        "fields": {
            "nm_slave": string,
            "ip_slave": string,
            "port"     : string
        }
    }
}
```
fields:
- nm_slave : slave device's name
- ip_slave : slave's IP address
- port      : Port used by slave device

example:
```
{
    "insert": {
        "fields": {
            "nm_slave": "slaveryiswrong",
            "ip_slave": "127.0.0.1",
            "port"     : "50"
        }
    }
}
```


### SLAVE WHERE

- path: /api/slave
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
            "id_slave": slave::id_slave,
            "nm_slave": slave::nm_slave,
            "ip_slave": slave::ip_slave

        }
    }
}
```
- id_slave: id of the slave that you're searching
- nm_slave: name of the slave that you're searching
- ip_slave: ip address of the slave that you're searching

example:
```
{
   "where": {
      "tags": {
      	"nm_slave": "mas_slave"
      }
      	
   }
}
```


### SLAVE REMOVE
- path: /api/slave
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
      	"id_slave": ttl::id_slave
      }
      	
   }
}
```
tags:
- id_slave: id of slave data that will be removed

example:
```
{
   "remove": {
      "tags": {
      	"id_slave": "402329670102745089"
      }
      	
   }
}
```