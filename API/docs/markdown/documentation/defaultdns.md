## USER SIDE
### USER
- path: /api/user/dnscreate
- method: post
- response: application/json
- body: raw
- roles: user
- usage: Create default dns configuration

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

## ADMIN SIDE
### ADMIN

- path: /api/admin/zone
- method: post
- response: application/json
- body: raw
- roles: admin
- usage: Add new zone

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

