# knot-cli




Command Line Interface for Restknot


## What is knot-cli






## Usage

List of available command on knot-cli

#### Create
```
create dns (--nm=NAME) [-i]
create record (--nm NAME) (--nm-zn ZONENAME) (--type=TYPE) (--ttl TTL) (--nm-con CON) [--nm-con-ser CONSER] 
```

Options : 
```
    -h --help                 Print usage
    --nm NAME                 Set DNS/record name
    -type=TYPE                Set DNS type
    --ttl TTL                 Set DNS TTL 
    --nm-zn ZONENAME          Set zone of new record
    -i --interactive          Interactive Mode
    --nm-con CON              Set content name
    --nm-con-ser CONSER       Set content serial name
```

#### List

```
ls ttl
ls type
ls record [--nm NAME]
ls dns
```

Options : 

```
--nm                        Show list of selected zone

```

#### Remove
```
rm dns (--nm NAME)
rm record [(--nm-zone=ZNNAME [--nm-record=NAME] [--type=TYPE] )]

```

<a name="Filter"></a>Options : 
```
-h --help               Print usage
--nm=NAME               DNS' name to delete
--nm-record=NAME        Filter record by record's name
--nm-zn=ZNNAME          Filter record by zone's name
```

### Login and Account
Knot-cli requires you to create an account on [portal-neo](https://portal.neo.id/). Note that before using knot-cli you have to login using

```
login
```
```
logout [-r]
```

use logout -r to remove all your data for fresh login in the future


### Creating Zone and Record

To create a new zone and records, use the following commands respectively 

```
create dns (--nm=NAME)
create record (--nm NAME) (--nm-zn ZONENAME) (--type=TYPE) (--ttl TTL) (--nm-con) [--nm-con-ser CONSER]
```

Remember to check available type and ttl before creating records, also MX and SRV record need serial content on creation. 


```
ls ttl
ls type
```



### Removing Zone and Record

```
rm dns (--nm NAME)
rm record [(--nm-zone=ZNNAME [--nm-record=NAME] [--type=TYPE] )]
```

When you're removing dns, knot-cli will give you a list of records that will also be removed and ask your confirmation.

On record removal, knot-cli will give you a list of your record based on filter (or all of your record if no filter is given). 

![knot-cli rm1](/docs/img/rm1.jpg?raw=True "Record removal")

Enter index of the record that you want to remove, then knot-cli will ask for your confirmation.

![knot-cli rm2](/docs/img/rm2.jpg "Record removal 2")


