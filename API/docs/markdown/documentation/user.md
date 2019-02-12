# USER ENDPOINT

User credential is obtained after you create an account in [portal-neo](https://portal.neo.id/)


### USER ALL
- path: /api/user
- method: get
- response: application/json
- body: no
- roles: all
- usage: Get all userdata

### CREATE USERDATA
- path: /api/user
- method: get
- response: application/json
- body: no
- roles: all
- usage: Get all userdata

### DELETE USERDATA
- path: /api/user/{userdata::userdata_id}
- method: delete
- response: application/json
- body: no
- roles: all
- usage: remove userdata

### GET BY ID USERDATA
- path: /api/user/{userdata::userdata_id}
- method: get
- response: application/json
- body: no
- roles: all
- usage: Get userdata by ID

### UPDATE USER DATA
- path: /api/user/{userdata::userdata_id}
- method: update
- response: application/json
- body: raw
- roles: all
- usage: remove userdata

raw
```
{
	"user_id": string,
	"project_id": string
}
```

- user_id: user id of your portal neo account
- project_id: project id of your portal neo account