## ADMIN

### ADMIN LOGIN

Before you use Admin endpoint, you have to whitelist your IP first by setting 'ACL' environment in app/middlewares/auth.py as follows

Multiple IP have to be separated by comma without whitespaces.

As administrator, you must not include access token each time you make a request. 

```python
os.environ["ACL"] = "First IP,SECOND IP"
```

Then you also have to set environment for your admin's username and password in app/controllers/api/admin/auth.py as follows :

```python
os.environ["ADMIN_USER"] = "your username"
os.environ["ADMIN_PASSWORD"] = "your password"
```

- path: /api/admin/login
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Login As Admin


raw :
```raw
{
   "username" : string,
   "password" : string,
   "project_id": string
}
```
fields:
- project_id: Your project id according your portal neo account

### ADMIN CREATE  DEFAULT DNS


- path: /api/admin/zone
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Add new zone as administrator with default configuration

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