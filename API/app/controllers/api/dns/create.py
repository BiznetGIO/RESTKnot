from flask_restful import Resource, reqparse, fields
from app.helpers.rest import *
from app.helpers.memcache import *
import datetime
from app.models import model as db
from app.libs.utils import repodefault
import datetime

def addSOADefault(zone):
    defaultdata = repodefault()
    zone_data = db.get_by_id("zn_zone","nm_zone", zone)
    type_data = db.get_by_id("zn_type","nm_type","SOA")

    # ADD SOA DEFAULT RECORD
    date = datetime.datetime.now().strftime("%Y%m%d%H")
    record_soa = {
        "nm_record": zone,
        "date_record": str(date),
        "id_zone":str(zone_data[0]['id_zone']),
        "id_type":str(type_data[0]['id_type'])
    }

    try:
        db.insert("zn_record", record_soa)
    except Exception as e:
        print(e)

    record_soa_data = db.get_by_id("zn_record","id_zone",zone_data[0]['id_zone'])
    ttldata_soa = {
        "id_record": str(record_soa_data[0]['id_record']),
        "id_ttl": "402140815780249601"
    }

    try:
        db.insert("zn_ttldata", ttldata_soa)
    except Exception as e:
         print(e)

    ttl_soa_data = db.get_by_id("zn_ttldata","id_record",record_soa_data[0]['id_record'])
    content_soa_d = defaultdata['default']['ns']
    for i in content_soa_d:
        content_soa = {
            "id_ttldata": str(ttl_soa_data[0]['id_ttldata']),
            "nm_content": i
        }
        try:
            db.insert("zn_content", content_soa)
        except Exception as e:
            print(e)

    serial_content_soa = defaultdata['default']['serial']
    for c in serial_content_soa:
        serial_content = {
            "nm_content_serial": c,
            "id_record": str(record_soa_data[0]['id_record'])
        }
        try:
            db.insert("zn_content_serial", serial_content)
        except Exception as e:
            print(e)


def addNSDefault(zone):
    zone_data = db.get_by_id("zn_zone","nm_zone", zone)
    type_data = db.get_by_id("zn_type","nm_type","NS")
    date = datetime.datetime.now().strftime("%Y%m%d%H")
    record_ns = {
        "nm_record": "@",
        "date_record": str(date),
        "id_zone":str(zone_data[0]['id_zone']),
        "id_type":str(type_data[0]['id_type'])
    }

    try:
        db.insert("zn_record", record_ns)
    except Exception as e:
        print(e)

    record_ns_data = db.get_by_id("zn_record","id_zone",zone_data[0]['id_zone'])
    for i in record_ns_data:
        if str(i['id_type']) ==  "402393625286410241":
            record_ns_data = i
    ttldata_ns = {
        "id_record": str(record_ns_data['id_record']),
        "id_ttl": "402140815780249601"
    }

    try:
        db.insert("zn_ttldata", ttldata_ns)
    except Exception as e:
        print(e)
    ttl_ns_data = db.get_by_id("zn_ttldata","id_record",str(record_ns_data['id_record']))
    content = repodefault()['default']['ns']

    for i in content:
        content_ns = {
            "id_ttldata": str(ttl_ns_data[0]['id_ttldata']),
            "nm_content": i
        }
        try:
            db.insert("zn_content", content_ns)
        except Exception as e:
            print(e)


class CreateDNS(Resource):
    # @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('domain', type=str, required=True)
        args = parser.parse_args()
        zone = args['domain']
        zone_domain = {
            'nm_zone': zone
        }
        check = False
        try:
            db.insert("zn_zone", zone_domain)
            check = True
        except Exception as e:
            msg = str(e)

        if not check:
            print(msg)
        else:
            addSOADefault(zone)
            addNSDefault(zone)
        respon = list()
        try:
            zone_data = db.get_by_id("zn_zone","nm_zone", zone)
        except Exception:
            data = {
                "status": False,
                "messages": str(e)
            }
            respon.append(data)
            return response(200, message=data)
        else:
            for i in zone_data:
                data = {
                    'id_zone': str(i['id_zone']),
                    'nm_zone': i['nm_zone']
                }
            respon = {
                "status": True,
                "data": data
            }
            return response(200, data=respon,message="Fine!")



