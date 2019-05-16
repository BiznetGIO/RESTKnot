# RECORD CONTENT

## A
```
A:
  example: 192.168.123.10
  content:
    params:
      IPv4:
        type: STR
        desc: An IPv4 address must be a decimal dotted quad string.
```

## AAAA
```
AAAA:
  example: 2001:db8::c0ff:e:e
  content:
    params:
      IPv6:
        type: STR
        desc: An IPv6 address must a coloned hex IPv6 address string.
```

## CNAME
```
CNAME:
  example: example.com
  content:
    params:
      hostname:
        type: STR
        desc: A hostname should be valid and may only contain A-Z, a-z, 0-9, _, -, and .. An MX record may never be an ip/ipv6 address, and must not point to a CNAME. Entering incorrect information here can negatively impact your ability to receive and in some cases send mail. A CNAME record must always point to another domain name, never directly to ip address
```
## MX
```
MX:
  example: 10 mail.example.com
  content:
    params:
      priority:
        type: STR
        desc: To differentiate them, each MX record has a priority (lower the number, higher the priority). The MX record with the highest priority is the actual target computer where mail boxes are located. '10' is a good default. 
  serial:
    params:
      hostname:
        type: STR
        desc: A hostname should be valid and may only contain A-Z, a-z, 0-9, _, -, and .. An mx may never be an ip/ipv6 address, and must not point to a cname. Entering incorrect information here can negatively impact your ability to receive and in some cases send mail. 
```
## TXT
```
TXT:
  example: "this is an example of TXT record"
  content:
    params:
      txtdata:
        type: STR
        desc: Text data may only contain printable ASCII characters. Very long lines will be automatically broken into multiple 255 character segments. 
```
## NS
```
NS:
  example: ns1.rincewind.com
  content:
    params:
      nameserver:
        type: STR
        desc: A nameserver should be valid and may only contain A-Z, a-z, 0-9, _, -, and .. 
```
## SOA
```
SOA:
  example: example.com sam.vimes.com 2018102107 86400 7200 3600000 86400
  content:
    params:
      nameserver:
        type: STR
        desc: The primary name server for the domain and should match the nameserver on NS-record. e.g 'example.com'
      email:
        type: STR
        desc: The e-mail address of the responsible party for the zone. Typically an email address with '@' character replaced with period. e.g 'sam.vimes.com'
  serial:
    params:
      serial: 
        type: STR
        desc: A timestamp that's updated whenever DNS zone changes. e.g 2018102107
      refresh:
        type: STR
        desc: A number of seconds before the zone should be refreshed. e.g 86400
      retry:
        type: STR
        desc: A number of seconds before a failed refresh should be retried. e.g 7200
      expire:
        type: STR
        desc: The upper limit in seconds before the zone is considered no longer authoritative. e.g 3600000
      ttl:
        type: STR
        desc: The negative result TTL (for example, how long a resolver should consider a negative result for a subdomain to be valid before retrying). e.g 86400
```
## SRV
```
SRV:
  example: 0 60 5060 bigbox.example.com.
  content:
    params:
      priority:
        type: str
        desc: The priority must only be within the range 0-65535 (lower is better ). 0 is a good default. 
  serial:
    params:
      weight:
        type: str
        desc: The weight must only be within the range 0-65535 (higher is better ). 0 is a good default. 
      port:
        type: str
        desc: The port must only be within the range 0-65535. The port varies depending on the service (ie 80, 5222, 5069, etc) 
      target:
        type: str
        desc: This is the hostname of the machine running the service. It should exist as an A record and may only contain A-Z, a-z, 0-9, _, -, and .. 
```




## Note
------------
According to [rfc1035](https://tools.ietf.org/html/rfc1035), there several rules that should be noted when filling record's field.

- An absolute url (FQDN) must end in dot (.)
- A relative domain (hostnames) does not end in dot.
- character '@' is used to denote current origin (root host), except in CNAME records


Example :

MX Record example

```
Domain/Content			    TTL   Priority      Host/Record Name
example.com.		        1936	10            blackmail
example.com.		        1936	10            whitemail
```

if value does not end in dot, it will be apppended to current zone.



### [Further Example](https://help.dnsmadeeasy.com/managed-dns/dns-record-types/)
