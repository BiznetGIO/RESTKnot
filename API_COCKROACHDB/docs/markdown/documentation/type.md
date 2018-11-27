# TYPE ENDPOINT
Zone consists of several endpoints including:

### TYPE ALL
- path : /api/type
- method : get
- response: application/json
- body: no
- roles: admin

Type all usage to get all data of record type

### TYPE ADD
- path : /api/type
- method : post
- response: application/json
- body: raw
- roles: admin

Function to enter one data in the type of DNS record type later
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
- nm_type

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
some examples of the type of record type you see Rules

### TYPE WHERE

- path : /api/type
- method : post
- response: application/json
- body: raw
- roles: admin

Function To Filtering Type Data
raw:
```
{
   "where": {
      "tags": {
      	"id_type": type::id_type
      }
   }
}
```

tags:
- id_type

Get One all data value for id_type
example:
```
{
   "where": {
      "tags": {
      	"id_type": "402329670102745089"
      }
      	
   }
}
```
### TYPE REMOVE
- path : /api/type
- method : post
- response: application/json
- body: raw
- roles: admin

Get Value Type Function 
raw:
```
{
   "remove": {
      "tags": {
      	"id_type": "402329670102745089"
      }
      	
   }
}
```
tags:
- id_type













