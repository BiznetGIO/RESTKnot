# CREATE RECORD

## A,CNAME,AAA,TXT RECORD
### create record
- endpoint: api/record
- method: post
- raw : json
```
{
   "insert": {
      "fields": {
      	"nm_record": string,
        "date_record": string, #format 2018070410
        "id_zone": zone::id_zone,
        "id_type": type::id_type
      }
      	
   }
}
```

- id_type : The type of the record that will be inserted. See [RULES](rules.md) for further information on available record type.
- id_zone : id of the zone in which record will be inserted. See [record](record.md) for further information.
- date_record: recommended using strftime function or equivalent.

example:
```
{
   "insert": {
      "fields": {
      	"nm_record":"pipit",
        "date_record":"2018070410",
        "id_zone":"402468020781678593",
        "id_type":"402386688803307521"
      }
      	
   }
}
```
nm_record must not be empty. If you're not planning to create a subdomain, please put '@' as nm_record

example:
```
{
   "insert": {
      "fields": {
      	"nm_record":"@",
        "date_record":"2018070410",
        "id_zone":"402468020781678593",
        "id_type":"402386688803307521"
      }
      	
   }
}
```

response:
```
{
    "count": 4,
    "data": {
        "id_zone": "402468020781678593",
        "id_type": "402386688803307521",
        "nm_record": "pipit",
        "date_record": "2018070410"
    },
    "code": 200,
    "status": "success",
    "message": {
        "status": true,
        "messages": "Fine!"
    }
}
```

### Connecting A,CNAME,AAA,TXT record to TTL Data

- endpoint: api/ttldata
- method: post
- raw : json
```
{
   "insert": {
      "fields": {
        "id_record": record::id_record,
        "id_ttl": ttl::id_ttl
      }
      	
   }
}
```

example:
```
{
   "insert": {
      "fields": {
        "id_record": "402475422581915649",
        "id_ttl": "402427994557939713"
      }
      	
   }
}
```

response:
```
{
    "count": 2,
    "data": {
        "id_ttl": "402427994557939713",
        "id_record": "402475422581915649"
    },
    "code": 200,
    "status": "success",
    "message": {
        "status": true,
        "messages": "Fine!"
    }
}
```

### Add Content For Your Record

- endpoint: api/content
- method: post
- raw : json
```
{
   "insert": {
      "fields": {
      	"id_ttldata": ttldata::id_ttldata,
        "nm_content": string
      }
      	
   }
}
```
keep in mind that the value of nm_content can be different according to the RECORD TYPE you entered, in this example the author uses an IP address because the record entered is type A

example:
```
{
   "insert": {
      "fields": {
      	"id_ttldata": "4024786369878017",
        "nm_content": "1.1.1.1"
      }
      	
   }
}
```

response:
```
{
    "count": 2,
    "data": {
        "id_ttldata": "402476086369878017",
        "nm_content": "1.1.1.1"
    },
    "code": 200,
    "status": "success",
    "message": {
        "status": true,
        "messages": "Fine!"
    }
}
```

### SYNC YOUR RECORD TO KNOT

- endpoint: api/sendcommand
- method: post
- raw : json
```
{
   "zone-insert": {
      "tags": {
      	"id_record" : record::id_record
      }
   }
}
```

example:
```
{
   "zone-insert": {
      "tags": {
      	"id_record" : "402475422581915649"
      }
   }
}
```

response:
```
{
    "count": 1,
    "data": [
        {
            "status": true,
            "command": [
                {
                    "zone-begin": [
                        {
                            "sendblock": {
                                "cmd": "zone-begin",
                                "zone": "mainburung.com"
                            }
                        },
                        {
                            "receive": {
                                "type": "block"
                            }
                        }
                    ]
                },
                {
                    "zone-set": [
                        {
                            "sendblock": {
                                "cmd": "zone-set",
                                "zone": "mainburung.com",
                                "owner": "pipit",
                                "rtype": "A",
                                "ttl": "14400",
                                "data": "1.1.1.1"
                            }
                        },
                        {
                            "receive": {
                                "type": "block"
                            }
                        }
                    ]
                },
                {
                    "zone-commit": [
                        {
                            "sendblock": {
                                "cmd": "zone-commit",
                                "zone": "mainburung.com"
                            }
                        },
                        {
                            "receive": {
                                "type": "block"
                            }
                        }
                    ]
                }
            ],
            "receive": {}
        }
    ],
    "code": 200,
    "status": "success",
    "message": "Operation succeeded"
}
```

### CHECKING YOUR CONFIGURATION

- endpoint: api/sendcommand
- method: post
- raw : json
```
{
   "zone-read": {
      "tags": {
      	"id_zone" : zone::id_zone
      }
   }
}
```

example:
```
{
   "zone-read": {
      "tags": {
      	"id_zone" : "402468020781678593"
      }
   }
}
```

response:
```
{
    "count": 1,
    "data": [
        {
            "status": true,
            "command": [
                {
                    "zone-read": [
                        {
                            "sendblock": {
                                "cmd": "zone-read",
                                "zone": "mainburung.com"
                            }
                        },
                        {
                            "receive": {
                                "type": "block"
                            }
                        }
                    ]
                }
            ],
            "receive": {
                "mainburung.com.": {
                    "mainburung.com.": {
                        "NS": {
                            "ttl": "86400",
                            "data": [
                                "ns1.biz.net.id.",
                                "hostmaster.biz.net.id."
                            ]
                        },
                        "SOA": {
                            "ttl": "86400",
                            "data": [
                                "ns1.biz.net.id. hostmaster.biz.net.id. 2018112223 10800 3600 604800 38400"
                            ]
                        }
                    },
                    "pipit.mainburung.com.": {
                        "A": {
                            "ttl": "14400",
                            "data": [
                                "1.1.1.1"
                            ]
                        }
                    }
                }
            }
        }
    ],
    "code": 200,
    "status": "success",
    "message": "Operation succeeded"
}
```

### Additional
```
A:
    content:
  	    IP:
            type: string
            example: "1.1.1.1"
CNAME:
	content:
  	    hostname:
            type: string
            example: "host.com
AAAA:
    content:
  	    IPv6:
            type: string
            example: "fe80::638f:c7a3:2545:6857"
NS:
    content:
        nameserver:
            type: string
            example: "ns1.biz.net.id."

```

## MX RECORD

The difference in the MX Type Record is that there is a serial on each record, the step to enter the same record until it completes entering the content



### ADD SERIAL CONTENT TO MX

The rule for filling in the MX Record is to give Value priority to the content then fill the hostname in the serial content.

- endpoint: api/serial_content
- method: post
- raw : json
```
{
   "insert": {
      "fields": {
      	"nm_content_serial": string,
        "id_record": record::id_record
      }
      	
   }
}
```
- note that my id_record is 402484026268352513


example:
```
{
   "insert": {
      "fields": {
      	"nm_content_serial": "host.com",
        "id_record": "402484026268352513"
      }
      	
   }
}
```

response:
```
{
    "count": 2,
    "data": {
        "nm_content_serial": "host.com",
        "id_record": "402484026268352513"
    },
    "code": 200,
    "status": "success",
    "message": {
        "status": true,
        "messages": "Fine!"
    }
}
```

### SYNC YOUR MX CONTENT

- endpoint: api/sendcommand
- method: post
- raw : json
```
{
   "zone-mx-insert": {
      "tags": {
      	"id_record" : "402468020781678593"
      }
   }
}
```

response:
```
{
    "count": 3,
    "data": [
        [
            {
                "status": true,
                "command": [
                    {
                        "zone-begin": [
                            {
                                "sendblock": {
                                    "cmd": "zone-begin",
                                    "zone": "mainburung.com"
                                }
                            },
                            {
                                "receive": {
                                    "type": "block"
                                }
                            }
                        ]
                    }
                ],
                "receive": {}
            }
        ],
        [
            {
                "status": true,
                "messages": "Block Type Command Execute"
            }
        ],
        [
            {
                "status": true,
                "command": [
                    {
                        "zone-read": [
                            {
                                "sendblock": {
                                    "cmd": "zone-commit",
                                    "zone": "mainburung.com"
                                }
                            },
                            {
                                "receive": {
                                    "type": "block"
                                }
                            }
                        ]
                    }
                ],
                "receive": {}
            }
        ]
    ],
    "code": 200,
    "status": "success",
    "message": "Operation succeeded"
}
```

### CHECK MX RECORD

- endpoint: api/sendcommand
- method: post
- raw : json
```
{
   "zone-read": {
      "tags": {
      }
   }
}
```

response:
```
{
    "count": 1,
    "data": [
        {
            "status": true,
            "command": [
                {
                    "zone-read": [
                        {
                            "sendblock": {
                                "cmd": "zone-read",
                                "zone": "mainburung.com"
                            }
                        },
                        {
                            "receive": {
                                "type": "block"
                            }
                        }
                    ]
                }
            ],
            "receive": {
                "mainburung.com.": {
                    "mainburung.com.": {
                        "NS": {
                            "ttl": "86400",
                            "data": [
                                "ns1.biz.net.id.",
                                "hostmaster.biz.net.id."
                            ]
                        },
                        "SOA": {
                            "ttl": "86400",
                            "data": [
                                "ns1.biz.net.id. hostmaster.biz.net.id. 2018112224 10800 3600 604800 38400"
                            ]
                        }
                    },
                    "pipit.mainburung.com.": {
                        "A": {
                            "ttl": "14400",
                            "data": [
                                "1.1.1.1"
                            ]
                        }
                    },
                    "tekukur.mainburung.com.": {
                        "MX": {
                            "ttl": "14400",
                            "data": [
                                "0 host.com.mainburung.com."
                            ]
                        }
                    }
                }
            }
        }
    ],
    "code": 200,
    "status": "success",
    "message": "Operation succeeded"
}
```

## OTHERS

- SRV records' synchronization is similar to MX RECORD except the body. See [documentation](sendcommand.md) for information

- See [documentation](RULES.md) for available record types and its content





