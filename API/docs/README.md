## API DOCUMENTATION
-------------------------
## Before You Begin
RESTKnot API requires you to be registered in neo portal. If you don't have an account yet, please create one [here](http://portal.neo.id)



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