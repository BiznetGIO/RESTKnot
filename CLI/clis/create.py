import os
from .base import Base
from libs import utils as util
from libs.list import check_zone_authorization
from libs import config as app
from libs.wrapper import *

class Create(Base):
    """
    usage:
        create dns (--nm=NAME) [-i]
        create record (--nm NAME) (--nm-zn ZONENAME) (--type=TYPE) (--ttl TTL) (--nm-con CON) [--nm-con-ser CONSER] 
        create record -f FILENAME

    Options :
    -h --help                 Print usage
    --nm NAME                 Set DNS/record name
    -type=TYPE                Set DNS type
    --ttl TTL                 Set DNS TTL 
    --nm-zn ZONENAME          Set zone of new record
    -i --interactive          Interactive Mode
    --nm-con CON              Set content name
    --nm-con-ser CONSER       Set content serial name
    -f FILENAME               Create Record using YAML

    Commands:
     dns                        Create DNS
     record                     Create record 
    
    """
    
    #@login_required
    def execute(self):
        if self.args['dns']:
            
            check = util.check_existence('zone',self.args['--nm'])
            if check['status']:
                print("ZONE ALREADY EXIST")
            else :
                if 'expired' in check['message']:
                    print(check['message'])
                else :
                    app.setDefaultDns(self.args['--nm'])

        elif self.args['record'] and not self.args['-f']:
            check = dict()
            skip = False
            nodata = ' '
            temp = check_zone_authorization([self.args['--nm-zn']])
            check['zone'] = temp['status']
            temp = util.check_existence('type',self.args['--type'].upper())
            check['type'] = temp['status']
            temp = util.check_existence('ttl',self.args['--ttl'])
            check['ttl'] = temp['status']

            if self.args['--type'].upper() == 'MX' or self.args['--type'].upper() == 'SRV':
                if self.args['--nm-con-ser'] is None:
                    util.log_warning("Record {} require serial content data".format(self.args['--type'].upper()))
                    exit()
            for i in check:
                if not check[i] :
                    nodata = nodata + i + ', '
                    skip = True
            
            if skip is True:
                print("Value of " + nodata + "doesn't exist. \nTry command ls to check available values")
            else: 
                self.args['--date'] = util.get_time()
                app.setRecord(self.args)
        elif self.args['record'] and self.args['-f']:
            path = self.args['-f']
            data = app.load_yaml(path)
            dnslist = list(data['data'].keys())
            check = check_zone_authorization(dnslist)
            sendlist = list()
            if 'data' not in check:
                sendlist = dnslist
                
            else :
                for i in dnslist:
                    if i not in check['data']:
                        sendlist.append(i)
            
            if sendlist:
                print(str(sendlist) + " doesn't exist. Do you want to create these dns and continue? (Y/N)")
                if util.assurance():
                    for i in sendlist:
                        app.setDefaultDns(i)
                else :
                    print("ABORT")
                    exit()


            data = app.parse_yaml(data['data'])
        
            send = data['data']
            for row in send:
                res=app.setRecord(row)
            
        