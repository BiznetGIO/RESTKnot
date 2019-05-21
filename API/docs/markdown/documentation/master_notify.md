# MASTER NOTIFY ENDPOINT


### GET MASTER NOTIFY
- path: /api/notify_master
- method: GET
- response: application/json
- body: no
- roles: admin
- usage: Get all available Master Notification

### INSERT MASTER NOTIFY
- path: /api/notify_master
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Add new Master Notification

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

- path: /api/notify_master
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Find master notification data by tag (id or name) for filtering. 

raw:
```
{
    "where": {
        "tags":{
            "id_master": master::id_master,
            "id_notify_master": master_notify::id_notify_master,
            "id_zone": zone::id_zone

        }
    }
}
```
- id_master: id master of the notification that you're searching
- id_notify_master: id of the notification that you're searching
- id_zone: id zone of the notification that you're searching

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
- path: /api/notify_master
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
      	"id_notify_master": master_notify::id_notify_master
      }
      	
   }
}
```
tags:
- id_notify_master: id of master notification data that will be removed

example:
```
{
   "remove": {
      "tags": {
      	"id_notify_master": "402329670102745089"
      }
      	
   }
}
```