from etcd import Client
import os

etcd_host = os.environ.get("ETCD_HOST", os.getenv("ETCD_HOST"))                                        
etcd_port = os.environ.get("ETCD_PORT", os.getenv("ETCD_PORT"))
client = Client(host=etcd_host, port=int(etcd_port))

# Execute in app start
# client.write('/user', None, dir=True)
# client.write('/ttl', None, dir=True)
# client.write('/type', None, dir=True)
# client.write('/zone', None, dir=True)
# client.write('/record', None, dir=True)
# client.write('/serial', None, dir=True)
# client.write('/conten', None, dir=True)


# client.write("/user/1", {"key": "1","email": "admin@biznetgio.com", "project_id": "001","state": "inserted", "created_at":"2019-07-20 23:04:22.420505"})
# client.write("/ttl/1", {"key": "1","value": "300"})
# client.write("/ttl/2", {"key": "2","value": "900"})
# client.write("/ttl/3", {"key": "3","value": "1800"})
# client.write("/ttl/4", {"key": "4","value": "3600"})
# client.write("/ttl/5", {"key": "5","value": "7200"})
# client.write("/ttl/6", {"key": "6","value": "14400"})
# client.write("/ttl/7", {"key": "7","value": "28800"})
# client.write("/ttl/8", {"key": "8","value": "43200"})
# client.write("/ttl/9", {"key": "9","value": "86400"})

# client.write("/type/1", {"key": "1","value": "A", "serial": False})
# client.write("/type/2", {"key": "2","value": "CNAME", "serial": False})
# client.write("/type/3", {"key": "3","value": "MX", "serial": True})
# client.write("/type/4", {"key": "4","value": "SOA", "serial": False})
# client.write("/type/5", {"key": "5","value": "NS", "serial": False})
# client.write("/type/6", {"key": "6","value": "TXT", "serial": False})
# client.write("/type/7", {"key": "7","value": "SRV", "serial": True})

client.watch("/type/1")
