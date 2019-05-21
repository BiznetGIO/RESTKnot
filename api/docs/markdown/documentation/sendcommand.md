# SENDCOMMAND ENDPOINT
The purpose of sendcommand is to synchronize records and zones with knot server.

For steps and practical example, see [rules](RULES_add_record.md)

Sendcommands consists of several endpoints including:

### CONF INSERT COMMAND
- path: /api/sendcommand
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Synchronize zone to knot server

raw
```
{
   "conf-insert": {
      "tags": {
      	"id_zone" : zone::id_zone
      }
   }
}
```
tags: id of target zone

### CONF READ 
- path: /api/sendcommand
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: To get whole configuration in knot server

raw:
```
{
   "conf-read": {
      "tags": {
      	
      }
   }
}
```
### ZONE READ

- path: /api/sendcommand
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Check configuration of specific zone in knot server

raw:
```
{
   "zone-read": {
      "tags": {
      	"id_zone" : zone::id_zone
      }
   }
}
```

tags:
- id_zone: id of the target zone

### ZONE BEGIN
- path: /api/sendcommand
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Start a writing transaction of specific zone in knot server
raw:
```
{
   "zone-begin": {
      "tags": {
      	"id_zone" : zone::id_zone
      }
   }
}
```
tags:
- id_zone: id of target zone

### ZONE COMMIT
- path: /api/sendcommand
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Commit transaction on specific zone in knot server

raw:
```
{
   "zone-commit": {
      "tags": {
      	"id_zone" : zone::id_zone
      }
   }
}
```
tags:
- id_zone: id of target zone


### SYNCHRONIZING RECORD
-------------------------------------
### IMPORTANT
Before you synchronize records to knot server, please look at the table below to see which endpoint you should use according to the record's type

| Record Type 	| Endpoint                       	|
|-------------	|--------------------------------	|
| SRV         	| zone-srv-insert                	|
| MX          	| zone-mx-insert                 	|
| SOA         	| zone-soa-insert                	|
| NS          	| zone-ns-insert,   zone-insert 	   |
| Other       	| zone-insert                    	|


### ZONE INSERT
- path: /api/sendcommand
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Synchronize record with types other than SOA,SRV,MX to knot server

raw:
```
{
   "zone-insert": {
      "tags": {
      	"id_record" : record::id_record
      }
   }
}
```
tags:
- id_record: id of target record

### ZONE SOA INSERT
- path: /api/sendcommand
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Synchronize SOA type record to knot server

raw:
```
{
   "zone-soa-insert": {
      "tags": {
      	"id_zone" : zone::id_zone
      }
   }
}
```
tags:
- id_zone: id of target zone

### ZONE SRV INSERT
- path: /api/sendcommand
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Synchronize SRV record to knot server

raw:
```
{
   "zone-srv-insert": {
      "tags": {
      	"id_record" : record::id_record
      }
   }
}
```
tags:
- id_record: id of target record


### ZONE NS INSERT
- path: /api/sendcommand
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Synchronize NS record to knot server

raw:
```
{
   "zone-ns-insert": {
      "tags": {
      	"id_record" : record::id_record
      }
   }
}
```
tags:
- id_record: id of target record

### ZONE MX INSERT
- path: /api/sendcommand
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Synchronize MX record to knot server

raw:
```
{
   "zone-mx-insert": {
      "tags": {
      	"id_record" : record::id_record
      }
   }
}
```
tags:
- id_record: id of target record


### CONF UNSET
- path: /api/sendcommand
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Unset configuration of target zone

raw:
```
{
   "conf-unset": {
      "tags": {
      	"id_zone" : zone::id_zone
      }
   }
}
```
tags:
- id_zone: id of target zone

### ZONE RECORD UNSET
- path: /api/sendcommand
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: unset specific record configuration on knot server

raw:
```
{
   "zone-unset": {
      "tags": {
      	"id_record" : record::id_record
      }
   }
}
```
tags:
- id_record: id of target record