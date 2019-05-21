# Test create and list
#
#
import pytest
import json
import os
from io import StringIO 
from dotenv import load_dotenv
import sys
#sys.path.append('/home/mfriszky/worksworksworks/branch-sandbox/RESTKnot/CLI')

from libs import config as app
from libs import listing as ls
from libs import utils as util
from libs import remove as delete

class TestCreate():
    @pytest.mark.run(order=0)
    def test_create_dns(self):
        new_zone = 'testclis.com'
        res = app.setDefaultDns(new_zone)
        dns = ls.list_dns()
        assert new_zone in dns['data']

    @pytest.mark.run(order=1)
    def test_create_record(self):
        mock_zone = ['testclis2.com','testclis.com']
        mock_type = ['tipe','CNAME']
        mock_ttl  = ['2200','7200']

        mock_data = list()
        passed = list()
        for zone in mock_zone:
            for tipe in mock_type:
                for ttl in mock_ttl:
                    mock_data.append({'--nm-zn' : zone,
                    '--type' : tipe, 
                    '--ttl': ttl,
                    '--nm' : 'test',
                    '--nm-con' : 'alias',
                    '--nm-con-ser':None})
        
        mock_data.append({'--nm-zn' : mock_zone[1],
                    '--type' : 'SRV', 
                    '--ttl': mock_ttl[1],
                    '--nm' : 'test',
                    '--nm-con' : 'alias',
                    '--nm-con-ser':'80 80 80 80'})
        
        mock_data.append({'--nm-zn' : mock_zone[1],
                    '--type' : 'MX', 
                    '--ttl': mock_ttl[1],
                    '--nm' : 'test',
                    '--nm-con' : 'alias',
                    '--nm-con-ser':'serialcontenttestdata'})
        for i in mock_data:
            if util.check_existence('zone',i['--nm-zn']):
                if (util.check_existence('type',i['--type']) and util.check_existence('ttl',i['--ttl'])):
                    passed.append(i)
                    #print(i)
        for i in passed:
            i['--date'] = util.get_time()
            app.setRecord(i)
        record_list = ls.list_record([mock_zone[1]])
        record_list = util.convert(record_list['data'])
        clean = util.table_cleanup(record_list)
        check = True
        for i in record_list:
            for j in passed:
                if j['--type'] == i['nm_type']:
                    check = bool(check and bool(j['--nm-zn'] and i['nm_zone']))
                    check = bool(check and bool(j['--nm'] and i['nm_record']))
                    check = bool(check and bool(j['--ttl'] and i['nm_ttl']))
                    check = bool(check and bool(j['--nm-con'] and i['nm_content']))
        assert check == True

    @pytest.mark.run(order=3)       
    def test_listing_filter(self):
        args = {
            '--nm-zone': 'testclis.com',
            '--nm-record' : 'test',
            '--type' : 'MX'
        }
        zone = [args['--nm-zone']]
        tags = args
        show = list()
        show = ls.list_record(zone,tags)
        show = util.convert(show['data'][0])
        assert show['nm_type'] == 'MX'
        assert show['nm_zone'] == 'testclis.com'
        assert show['nm_record'] == 'test'

    @pytest.mark.run(order=4)
    def test_record(self):
        zone = ['testclis.com']
        show = ls.list_record(zone)
        id_record = list()
        show = util.convert(show)
        show = show['data']
        for i in show :
            id_record.append(i['id_record'])
        index = [1,8]
        index = util.check_availability(index, (len(show)))
        id_record.pop()
        delete.remove_record(id_record)

    @pytest.mark.run(order=5)
    def test_list_dns(self):
        dnslist = ls.list_dns()
        dnslist = dnslist['data']
        assert 'testclis.com' in dnslist

    @pytest.mark.run(order=6)
    def test_get_data(self):
        result = ls.get_data('ttl',tags='nm_ttl',value='1800')
        result = result['data'][0]
        assert result['nm_ttl'] == '1800'


    @pytest.mark.run(order=7)
    def test_remove(self):
        res = delete.remove_zone('testclis.com')
        print(res)
        result = util.check_existence('zone','testclis.com')
        #assert result == False

    @pytest.mark.run(order=8)
    def test_listing_endpoint(self):
        st = ls.listing_endpoint('ttl')
        assert st != "No value available"

    
    def test_create_from_file(self):
        filename = 'create.yaml'
        data = app.load_yaml(filename)
        
        dnslist = list(data['data'].keys())
        print(dnslist)
        check = ls.check_zone_authorization(dnslist)

        sendlist = list()

        if 'data' not in check:
            sendlist = dnslist
        
        else :
            for dns in dnslist:
                if dns not in check['data']:
                    sendlist.append(dns)

        if sendlist:
            for dns in sendlist:
                app.setDefaultDns(dns)
        data = app.parse_yaml(data['data'])

        send = data['data']
        
        check = bool(True)
        for row in send:
            res = app.setRecord(row)
            check = check and res['status']
        assert check == True
        self.cleanup(dnslist)


    def cleanup(self,dnslist):
        for dns in dnslist:
            delete.remove_zone(dns)