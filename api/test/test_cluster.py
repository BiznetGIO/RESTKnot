import pytest
import json
import utils
import os
from app.helpers import cluster_master as cm
from app.helpers import cluster_slave as cs

class TestCluster:

    mock_zone = {
            "id_zone": "473169861404852225",
            "nm_zone": "testdns1.com",
            "state": 1
        }


    def test_insert_config_zone(self):

        data_zone = self.mock_zone
        res = cm.insert_config_zone(data_zone,'config_test')
        expected_result = {'command-set': {'sendblock': {'cmd': 'conf-set', 'item': 'domain', 'section': 'zone', 'data': 'testdns1.com'}, 'receive': {'type': 'block'}}}
        assert res == expected_result

    def test_create_json(self,client,get_header):
        data_zone = self.mock_zone

        res = cm.master_create_json_master(data_zone,'jkt')
        expected_result = {'master-set-master': {'sendblock': {'cmd': 'conf-set', 'zone': 'testdns1.com', 'item': 'master', 'owner': '', 'rtype': '', 'ttl': '', 'flags': '', 'section': 'zone', 'data': 'cmg01z00knms001'}, 'receive': {'type': 'block'}}}
        assert res == expected_result

        res = cm.master_create_json_notify(data_zone,'jkt','None')
        expected_result = [{'master-set-notify': {'sendblock': {'cmd': 'conf-set', 'zone': 'testdns1.com', 'item': 'notify', 'section': 'zone', 'data': 'cmg01z00knms001'}, 'receive': {'type': 'block'}}}, {'master-set-notify': {'sendblock': {'cmd': 'conf-set', 'zone': 'testdns1.com', 'item': 'notify', 'section': 'zone', 'data': 'jkt01z00knsl001'}, 'receive': {'type': 'block'}}}]
        assert res == expected_result

        res = cm.set_file_all(data_zone)
        expected_result = {'file-set': {'sendblock': {'cmd': 'conf-set', 'zone': 'testdns1.com', 'item': 'file', 'owner': '', 'rtype': '', 'ttl': '', 'identifier': 'testdns1.com', 'section': 'zone', 'data': 'testdns1.com_473169861404852225.zone'}, 'receive': {'type': 'block'}}}
        assert res == expected_result

        res = cm.set_mods_stats_all(data_zone,'data')
        expected_result = {'modstat-set': {'sendblock': {'cmd': 'conf-set', 'zone': 'testdns1.com', 'item': 'module', 'owner': '', 'rtype': '', 'ttl': '', 'flags': '', 'section': 'zone', 'data': 'data'}, 'receive': {'type': 'block'}}}
        assert res == expected_result

        res = cm.set_serial_policy_all(data_zone,'data')
        expected_result = {'serial-set': {'sendblock': {'cmd': 'conf-set', 'zone': 'testdns1.com', 'item': 'serial-policy', 'owner': '', 'rtype': '', 'ttl': '', 'flags': '', 'section': 'zone', 'data': 'data'}, 'receive': {'type': 'block'}}}
        assert res == expected_result

        res = cm.master_create_json_acl(data_zone,'jkt','test')
        expected_result = [{'master-set-acl': {'sendblock': {'cmd': 'conf-set', 'zone': 'testdns1.com', 'item': 'acl', 'section': 'zone', 'data': 'cmg01z00knms001'}, 'receive': {'type': 'block'}}}, {'master-set-acl': {'sendblock': {'cmd': 'conf-set', 'zone': 'testdns1.com', 'item': 'acl', 'section': 'zone', 'data': 'jkt01z00knsl001'}, 'receive': {'type': 'block'}}}]

        assert res == expected_result


    def test_slave_cluster(self):


        data_zone = self.mock_zone
        res = cs.insert_config_zone(data_zone)
        expected_result = {'command-set': {'sendblock': {'cmd': 'conf-set', 'item': 'domain', 'section': 'zone', 'data': 'testdns1.com'}, 'receive': {'type': 'block'}}}
        assert res == expected_result

        res = cs.master_create_json(data_zone,'jkt')
        expected_result = {'slave-set-master': {'sendblock': {'cmd': 'conf-set', 'zone': 'testdns1.com', 'item': 'master', 'section': 'zone', 'data': 'jkt'}, 'receive': {'type': 'block'}}}
        assert res == expected_result

        res = cs.create_json_notify(data_zone,'jkt')
        expected_result = {'slave-set-notify': {'sendblock': {'cmd': 'conf-set', 'zone': 'testdns1.com', 'item': 'notify', 'section': 'zone', 'data': 'jkt'}, 'receive': {'type': 'block'}}}
        assert res == expected_result

        res = cs.create_json_acl(data_zone,'jkt')
        expected_result =   {'slave-set-notify': {'sendblock': {'cmd': 'conf-set', 'zone': 'testdns1.com', 'item': 'acl', 'section': 'zone', 'data': 'jkt'}, 'receive': {'type': 'block'}}}
        assert res == expected_result
