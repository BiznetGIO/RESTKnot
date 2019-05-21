## CREATE DOMAIN
endpoint : api/user/dnscreate

Form :
- domain : string

method: post

response:
```
{
    "count": 2,
    "data": {
        "status": true,
        "data": {
            "id_zone": "402468020781678593",
            "nm_zone": "mainburung.com"
        }
    },
    "code": 200,
    "status": "success",
    "message": "Fine!"
}
```
### NOTE : 
dnscreate endpoint will automatically synchronize your SOA, CNAME and NS to the knot server. However, if you insert dns [manually](zone.md) (with zone endpoint, you have to synchronize the default records first).


## SYNC DOMAIN TO KNOT
After inserting your domain in API, synchronize it to Knot server

endpoint: api/sendcommand

method: post

raw : json
```json
{
   "conf-insert": {
      "tags": {
      	"id_zone" : string
      }
   }
}
```

response:
```json
{
    "count": 1,
    "data": [
        {
            "status": true,
            "command": [
                {
                    "conf-begin": [
                        {
                            "sendblock": {
                                "cmd": "conf-begin"
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
                    "conf-set": [
                        {
                            "sendblock": {
                                "cmd": "conf-set",
                                "section": "zone",
                                "item": "domain",
                                "data": "mainburung.com"
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
                    "conf-commit": [
                        {
                            "sendblock": {
                                "cmd": "conf-commit"
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

## SYNC DEFAULT RECORD SOA TO KNOT

DNS came with three default records: SOA,NS and CNAME.
You need to synchronize these records to knot server which will be explained in the following steps.

endpoint: api/sendcommand

method: post

raw : json
```json
{
   "zone-soa-insert": {
      "tags": {
      	"id_zone" : string
      }
   }
}
```

response:
```json
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

## SYNC DEFAULT RECORD NS TO KNOT
After Sync SOA records, synchronize the NS record to knot.

endpoint: api/sendcommand

method: post

raw : json
```json
{
   "zone-ns-insert": {
      "tags": {
      	"id_zone" : string
      }
   }
}
```

response:
```json
{
    "count": 2,
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
                    },
                    {
                        "zone-set": [
                            {
                                "sendblock": {
                                    "cmd": "zone-set",
                                    "zone": "mainburung.com",
                                    "owner": "@",
                                    "rtype": "NS",
                                    "ttl": "86400",
                                    "data": "ns1.biz.net.id."
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
                    },
                    {
                        "zone-set": [
                            {
                                "sendblock": {
                                    "cmd": "zone-set",
                                    "zone": "mainburung.com",
                                    "owner": "@",
                                    "rtype": "NS",
                                    "ttl": "86400",
                                    "data": "hostmaster.biz.net.id."
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
        ]
    ],
    "code": 200,
    "status": "success",
    "message": "Operation succeeded"
}
```

## SYNC DEFAULT RECORD CNAME TO KNOT

After Sync NOW check Your Config

endpoint: api/sendcommand

method: post

raw : json

```json
{
   "zone-insert": {
      "tags": {
      	"id_record" : "422446146700443649"
      }
   }
}
```



## CHECK YOUR DOMAIN AFTER SYNC TO KNOT

After Sync NOW check Your Config

endpoint: api/sendcommand

method: post

raw : json
```json
{
   "zone-read": {
      "tags": {
      	"id_zone" : string
      }
   }
}
```

respone:
```json
{
    "count": 3,
    "data": [
        {
            "data": {},
            "status": "Command Execute",
            "result": true,
            "Description": [
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
            ]
        },
        {
            "data": {},
            "status": "Command Execute",
            "result": true,
            "Description": [
                {
                    "zone-set": [
                        {
                            "sendblock": {
                                "rtype": "CNAME",
                                "data": "mainburung.com.",
                                "owner": "www",
                                "ttl": "86400",
                                "zone": "mainburung.com",
                                "cmd": "zone-set"
                            }
                        },
                        {
                            "receive": {
                                "type": "block"
                            }
                        }
                    ]
                }
            ]
        },
        {
            "data": {},
            "status": "Command Execute",
            "result": true,
            "Description": [
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
            ]
        }
    ],
    "code": 200,
    "status": "success",
    "message": "Operation succeeded"
}
```

response:
```json
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
                    "www.mainburung.com.": {
                    "CNAME": {
                        "data": [
                            "mainburung.com."
                        ],
                        "ttl": "86400"
                    }
                },
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
                                "ns1.biz.net.id. hostmaster.biz.net.id. 2018112222 10800 3600 604800 38400"
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