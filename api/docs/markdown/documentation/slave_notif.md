# SLAVE NOTIFY ENDPOINT


### GET SLAVE NOTIFY
- path: /api/notify_slave
- method: GET
- response: application/json
- body: no
- roles: admin
- usage: Get all available Slave Notify

### INSERT SLAVE NOTIFY
- path: /api/notify_slave
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Add new Slave Notify

raw:
```
{
    "insert": {
        "fields": {
            "id_notify_master": master_notify::id_notify_master,
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
            "id_notify_master": "402152439123235692",
            "id_slave": "402152439124393985"
        }
    }
}
```


### SLAVE NOTIFY WHERE

- path: /api/notify_slave
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Find slave Notify data by tag (id or name) for filtering. 

raw:
```
{
    "where": {
        "tags":{
            "id_slave": slave::id_slave,
            "id_notify_slave": slave_notify::id_notify_slave
        }
    }
}
```
- id_slave: id slave of the notification that you're searching
- id_notify_slave: id of the notification that you're searching

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


### SLAVE NOTIFY REMOVE
- path: /api/notify_slave
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
      	"id_notify_slave": slave_notify::id_notify_slave
      }
      	
   }
}
```
tags:
- id_notify_slave: id of notification slave data that will be removed

example:
```
{
   "remove": {
      "tags": {
      	"id_notify_slave": "402329670102745089"
      }
      	
   }
}
```