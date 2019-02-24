import pytest
import json
from app import db
from app.models import model

def getId(self,client,namethis,tokentest):
    res = client.get('api/zone',headers = tokentest)
    data = json.loads(res.data.decode('utf8'))
    print(data)
    for result in data['data']:
        if(result['nm_zone'] == namethis):
            id_result = result['id_zone']
    return id_result



def get_cleanup_id(domainname):
    obj_userdata= list()
    column = model.get_columns("v_all_content")
    query = "SELECT * FROM v_all_content WHERE nm_zone = \'"+domainname+"""\'"""
    try:
        result = list()
        db.execute(query)
        rows = db.fetchall()
        for row in rows:
            result.append(dict(zip(column,row)))
        
    except Exception as e:
        respons = {
            "status" : False,
            "messages":str(e)
        }
    else:
        for i in result:
            data = {
                "id_zone": str(i['id_zone']),
                "id_content": str(i['id_content']),
                "id_content_serial": str(i['id_content_serial']),
                "id_ttldata": str(i['id_ttldata']),
                "id_record": str(i['id_record'])
            }
            obj_userdata.append(data)    
    finally:
        return obj_userdata



class TestDNS:
    def test_dns_post_duplicate(self,client):
        data = {
            'domain' : 'catiskucing.com'
        }
        res = client.post('api/user/dnscreate', data = data )
        result = json.loads(res.data.decode('utf8'))
        print(result)
        assert result['code'] == 200

    def test_dns_post_(self,client):
        data = {
            'domain' : 'kucing.com'
        }
        res = client.post('api/user/dnscreate', data=data)
        result = json.loads(res.data.decode('utf8'))
        assert result['code'] == 200

    #def test_cleanup(self,client,tokentest):
        # ids = get_cleanup_id('kucing.com')
        # id_content = list()
        # id_content_serial = list()
        # id_ttldata = list()
        # id_record = list()
        # for id in ids:
        #     if id['id_content'] not in id_content:
        #         id_content.append(id['id_content'])
        #     if id['id_content_serial'] not in id_content_serial and id['id_content_serial'] != 'None':
        #         id_content_serial.append(id['id_content_serial'])
        #     if id['id_ttldata'] not in id_ttldata:
        #         id_ttldata.append(id['id_ttldata'])
        #     if id['id_record'] not in id_record:
        #         id_record.append(id['id_record'])

        # print ("HOOO ",ids)
        # id_zone = ids[0]['id_zone']

        # for content in id_content:
        #     res = client.post(
        #         'api/content',data=json.dumps({"remove":{"tags":{"id_content" : content}}}),
        #         headers = tokentest
        #     )
        # for ttldata in id_ttldata:
        #     res = client.post(
        #         'api/ttldata',data=json.dumps({"remove":{"tags":{"id_ttldata" : ttldata}}}),
        #         headers = tokentest
        #     )
        # for content_serial in id_content_serial:
        #     res = client.post(
        #         'api/content_serial',data=json.dumps({"remove":{"tags":{"id_content_serial" : content_serial}}}),
        #         headers = tokentest
        #     )
        # for record in id_record:
        #     res = client.post(
        #         'api/record',data=json.dumps({"remove":{"tags":{"id_record" : record}}}),
        #         headers = tokentest
        #     )
        # res = client.post(
        #         'api/zone',data=json.dumps({"remove":{"tags":{"id_zone" : id_zone}}}),
        #         headers = tokentest
        #     )
    def test_zone_post_remove(self,client,tokentest):
        delete_id = getId(self,client,'kucing.com',tokentest)
        json_rem = {
                        "remove": {
                            "tags": {
                                "id_zone": delete_id
                            }
                                
                        }
                    }
        res = client.post('api/zone', 
                            data=json.dumps(json_rem), 
                            content_type = 'application/json',
                            headers = tokentest
                            )

        assert res.status_code == 200
        