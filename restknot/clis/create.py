import os
from .base import Base
from libs import utils as util
from libs import config as app
from libs.wrapper import *

class Create(Base):
    """
    usage:
        create dns (--nm=NAME) [-i]
        create record (--nm NAME) (--nm-zn ZONENAME) (--type=TYPE) (--ttl TTL) [-i] [--nm-con CON] [--nm-con-ser CONSER] 

    Options :
    -h --help                                      Print usage
    --nm NAME                               Set DNS/record name
    -type=TYPE                              Set DNS type
    --ttl TTL                                       Set DNS TTL 
    --nm-zn ZONENAME          Set zone of new record
    -i --interactive                         Interactive Mode
    --nm-con CON                        Set content name
    --nm-con-ser CONSER       Set content serial name

    Commands:
     dns                        Create DNS
     record                     Create record 
    
    """
    
    @login_required
    def execute(self):
        if self.args['dns']:
            app.setDefaultDns(self.args['--nm'])

        elif self.args['record']:
            check = dict()
            skip = False
            nodata = ' '
            check['zone'] = util.check_existence('zone',self.args['--nm-zn'])
            check['type'] = util.check_existence('type',self.args['--type'].upper())
            check['ttl'] = util.check_existence('ttl',self.args['--ttl'])
            for i in check:
                if not check[i] :
                    nodata = nodata + i + ', '
                    skip = True
            
            if skip is True:
                print("Value of " + nodata + "doesn't exist. \nTry command ls to check available values")
            else: 
                self.args['--date'] = util.get_time()
                app.setRecord(self.args)
                print(self.args)
                
        