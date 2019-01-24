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

    Options :
    -h --help                 Print usage
    --nm NAME                 Set DNS/record name
    -type=TYPE                Set DNS type
    --ttl TTL                 Set DNS TTL 
    --nm-zn ZONENAME          Set zone of new record
    -i --interactive          Interactive Mode
    --nm-con CON              Set content name
    --nm-con-ser CONSER       Set content serial name

    Commands:
     dns                        Create DNS
     record                     Create record 
    
    """
    
    #@login_required
    def execute(self):
        if self.args['dns']:
            if util.check_existence('zone',self.args['--nm']):
                print("Zone already exist, try again")
            else :
                app.setDefaultDns(self.args['--nm'])

        elif self.args['record']:
            check = dict()
            skip = False
            nodata = ' '
            check['zone'] = check_zone_authorization([self.args['--nm-zn']])
            check['type'] = util.check_existence('type',self.args['--type'].upper())
            check['ttl'] = util.check_existence('ttl',self.args['--ttl'])


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
                
        