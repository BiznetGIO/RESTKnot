# import pytest
# import json


# class TestCommand:
#     def test_command_conf_ins(self,client):
#         json_1={
#                 "conf-insert": {
#                     "tags": {
#                         "domain_id" : "rosa.com"
#                     }
#                 }
#                 }
#         res = client.post('api/sendcommand', data=json.dumps(json_1), content_type='application/json')
#         assert res.status_code == 200

#     def test_command_zone_read(self,client):
#         json_comm_read={
#                         "zone-read": {
#                             "tags": {
#                                 "domain_id" : "rosa.com"
#                             }
#                         }
#                         }
#         res = client.post('api/sendcommand', data=json.dumps(json_comm_read), content_type='application/json')
#         assert res.status_code == 200

#     def test_command_zone_begin(self,client):
#         json_zone_begin={
#                         "zone-begin": {
#                             "tags": {
#                                 "domain_id" : "rosa.com"
#                             }
#                         }
#                         }
#         res = client.post('api/sendcommand',data=json.dumps(json_zone_begin),content_type='application/json')
#         assert res.status_code == 200

#     def test_command_soa_insert_command(self,client):
#         json_soa_insert={
#                         "zone-soa-insert": {
#                             "tags": {
#                                 "zone_id" : "rosa.com",
#                                 "ttl_data_id": "002"
#                             }
#                         }
#                         }

#         res = client.post('api/sendcommand',data=json.dumps(json_soa_insert),content_type='application/json')
#         assert res.status_code == 200