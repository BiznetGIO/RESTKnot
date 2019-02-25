## API DOCUMENTATION
-------------------------
## Before You Begin
RESTKnot API requires you to be registered in neo portal. If you don't have an account yet, please create one [here](http://portal.neo.id)


## IMPORTANT NOTE

If you're not logged in as admin, you have to include Access-Token in your headers each time you're making a request.

Headers : 
```raw
"Access-Token" : string
```

Access Token is generated each time you login via the following endpoint:

- path: /api/login
- method: post
- response: application/json
- body: raw
- roles: all
- usage: Login

raw:
```raw
{
    "username" : string,
    "password" : string
}
```

which will returns 

```
{
    "count": 3,
    "data": {
        "user_id": "your user id",
        "project_id": "your project id",
        "token": "access token"
    },
    "code": 200,
    "status": "success",
    "message": "Operation succeeded"
}
```

## API Endpoints
------------------
- **[ZONE](markdown/documentation/zone.md)** : Manages DNS
- **[TTL](markdown/documentation/ttl.md)** : Manages available TTL values
- **[TYPE](markdown/documentation/type.md)** : Manages available record types
- **[RECORD](markdown/documentation/record.md)** : Manages DNS' record
- **[TTLDATA](markdown/documentation/ttldata.md)** : Manages TTL values for available records
- **[CONTENT](markdown/documentation/content_data.md)**: Manages record's content
- **[CONTENT_SERIAL](markdown/documentation/content_serial.md)**: Manages serial data for MX and SRV records
- **[COMMAND](markdown/documentation/sendcommand.md)**: Synchronizing records and dns to knot server
- **[DEFAULTDNS](markdown/documentation/defaultdns.md)**: Creating DNS with default configuration. DNS that's created with this endpoint is automatically synchronized to knot server
- **[USER](markdown/documentation/user.md)**: Manages users credentials. User have to had portal neo account.
- **[ADMIN](markdown/documentation/admin.md)**:
Using Endpoint as administrator

## RULES
------------------
- ### Creating Domain :
    Steps needed to create and synchronize DNS is explained [here](RULES_add_domain.md)
- ### Creating Record :
    Steps needed to create and synchronize records is explained [here](RULES_add_record.md)
- ### Record Data :
    Required data for various type of records is explained [here](RULES.md)

## Others:
- Postman API Documentation : [link](postman/REST_KNOT_COCKROACH.json)

- Endpoint Data Structure : [link](markdown/data_structure/STRUCTURE_DATA.md)