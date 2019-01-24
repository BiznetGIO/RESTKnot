# knot-cli




Command Line Interface for Restknot


## What is knot-cli






## Usage

### Login and Account
Knot-cli requires you to create an account on [portal-neo] (https://portal.neo.id/). Note that before using knot-cli you have to login using

```
knot-cli login
```

### Creating Zone and Record

To create a new zone and records, use the following commands respectively 

```
create dns (--nm=NAME)
create record (--nm NAME) (--nm-zn ZONENAME) (--type=TYPE) (--ttl TTL) (--nm-con) [--nm-con-ser CONSER]
```

Remember to check available type and ttl before creating records 

```
ls ttl
ls type
```

MX and SRV need serial content upon creation. 
