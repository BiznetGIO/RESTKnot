import pytest
import json
from app.helpers import cmd_parser as parse


class TestCommand:
    def test_command_conf_ins(self,client,tokentest):
        json_1={
                "conf-insert": {
                    "tags": {
                        "id_zone" : "406644798852005889"
                    }
                }
                }
        res = client.post('api/sendcommand', data=json.dumps(json_1), content_type='application/json', headers = tokentest)
        assert res.status_code == 200

    def test_command_conf_read(self,client,tokentest):
        dataSend = {
                    "conf-read": {
                        "tags": {
                            
                            }
                        }
                    }
        res = client.post('api/sendcommand', data=json.dumps(dataSend), content_type='application/json', headers = tokentest)
        assert res.status_code == 200
    
    
    def test_command_zone_read(self,client,tokentest):
        json_comm_read={
                        "zone-read": {
                            "tags": {
                                "id_zone" : "406644798852005889"
                                }
                            }
                        }
        res = client.post('api/sendcommand', data=json.dumps(json_comm_read), content_type='application/json', headers = tokentest)
        assert res.status_code == 200

    def test_command_zone_begin(self,client,tokentest):
        json_zone_begin={
                        "zone-begin": {
                            "tags": {
                                "id_zone" : "406644798852005889"
                            }
                        }
                        }
        res = client.post('api/sendcommand',data=json.dumps(json_zone_begin),content_type='application/json', headers = tokentest)
        assert res.status_code == 200

#     def test_command_zone_insert(self,client):
#         print('BEGIN')
#         json_send={
#                     "zone-insert": {
#                         "tags": {
#                             "id_record" : "402475422581915649"
#                         }
#                     }
#                     }
        
#         res = client.post('api/sendcommand',data=json.dumps(json_send),content_type='application/json')
#         assert res.status_code == 200


    def test_command_zone_commit(self,client,tokentest):
        json_zone_begin={
                        "zone-commit": {
                            "tags": {
                                "id_zone" : "406644798852005889"
                            }
                        }
                        }
        res = client.post('api/sendcommand',data=json.dumps(json_zone_begin),content_type='application/json', headers = tokentest)
        assert res.status_code == 200

#     # def test_command_zone_ns_insert(self,client):
#     #     json_zone_begin={
#     #                     "zone-ns-insert": {
#     #                         "tags": {
#     #                             "record_data_id" : "1"
                                
#     #                         }
#     #                     }
#     #                     }
#     #     res = client.post('api/sendcommand',data=json.dumps(json_zone_begin),content_type='application/json')
#     #     assert res.status_code == 200


    def test_command_conf_read(self,client,tokentest):
        json_soa_insert={
                            "conf-read": {
                                "tags": {
                                    
                                }
                            }
                        }

        res = client.post('api/sendcommand',data=json.dumps(json_soa_insert),content_type='application/json', headers = tokentest)
        assert res.status_code == 200

    def test_command_zone_soa_insert(self,client,tokentest):
        json_zone_begin={
                        "zone-soa-insert": {
                            "tags": {
                                "id_zone" : "407780821838364673"
                            }
                        }
                        }
        res = client.post('api/sendcommand',data=json.dumps(json_zone_begin),content_type='application/json', headers = tokentest)
        assert res.status_code == 200

    def test_command_zone_insert(self,client,tokentest):
        json_insert={
                        "zone-insert": {
                            "tags": {
                                "id_record" : "407780821893644289",
                                "id_zone" : "407780821838364673"
                            }
                        }
                        }
        res = client.post('api/sendcommand', data=json.dumps(json_insert),content_type='application/json', headers = tokentest)
        assert res.status_code == 200

    def test_command_zone_ns_insert(self,client,tokentest):
        json_insert={
                        "zone-ns-insert": {
                            "tags": {
                                "id_zone" : "407780821838364673"
                            }
                        }
                        }
        res = client.post('api/sendcommand', data=json.dumps(json_insert),content_type='application/json', headers = tokentest)
        assert res.status_code == 200


    def test_command_zone_srv_insert(self,client,tokentest):
        json_insert={
                        "zone-srv-insert": {
                            "tags": {
                                "id_zone" : "407780821838364673"
                            }
                        }
                        }
        res = client.post('api/sendcommand', data=json.dumps(json_insert),content_type='application/json', headers = tokentest)
        assert res.status_code == 200

    def test_command_zone_mx_insert(self,client,tokentest):
        json_insert={
                        "zone-mx-insert": {
                            "tags": {
                                "id_zone" : "407780821838364673"
                            }
                        }
                        }
        res = client.post('api/sendcommand', data=json.dumps(json_insert),content_type='application/json', headers = tokentest)
        assert res.status_code == 200

    @pytest.mark.xfail
    def test_command_zone_mx_insert_fail(self,client,tokentest):
        json_insert={
                        "zone-mx-insert": {
                            "tags": {
                                "id_zone" : "403087427360391169"
                            }
                        }
                        }
        res = client.post('api/sendcommand', data=json.dumps(json_insert),content_type='application/json', headers = tokentest)
        assert res.status_code == 200
