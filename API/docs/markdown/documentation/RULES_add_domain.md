## CREATE DOMAIN
enpoint : api/user/dnscreate

form :
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

## SYNC DOMAIN TO KNOT
After your upload domain i API Now Syncronize Your To Knot

endpoint: api/sendcommand

method: post

raw : json
```
{
   "conf-insert": {
      "tags": {
      	"id_zone" : string
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
After Sync Domain Now Sync Default Record SOA

endpoint: api/sendcommand

method: post

raw : json
```
{
   "zone-soa-insert": {
      "tags": {
      	"id_zone" : string
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

## SYNC DEFAULT RECORD NS TO KNOT
After Sync Domain Now Sync Default Record NS

endpoint: api/sendcommand

method: post

raw : json
```
{
   "zone-ns-insert": {
      "tags": {
      	"id_zone" : string
      }
   }
}
```

response:
```
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


## CHECK YOUR DOMAIN AFTER SYNC TO KNOT

After Sync NOW check Your Config

endpoint: api/sendcommand

method: post

raw : json
```
{
   "zone-read": {
      "tags": {
      	"id_zone" : string
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