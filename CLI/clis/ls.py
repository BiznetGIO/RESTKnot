import os
from .base import Base
from libs import utils as util
from libs import config as app
from libs import list as sort
from libs.wrapper import *
import string
from tabulate import tabulate

class Ls(Base):
    """
    usage:
        ls ttl
        ls type
        ls record [--nm NAME]
        ls dns

    Options :
    
    --nm                        Show list of selected zone

    Commands:
     ttl                        List available ttl
     type                       List available type 
    
    """
    #@login_required
    def execute(self):
        if self.args['ttl'] :
            vallist = sort.listing_endpoint('ttl')
            print('Available TTL values are : ')
            print(vallist)
        elif self.args['type']:
            vallist = sort.listing_endpoint('type')
            print('Available Types are : ')
            print(vallist)
        elif self.args['dns']:
            vallist = sort.list_dns()
            print('Your Domains List Are : ')
            print(vallist)
        elif self.args['record'] :
            if self.args['--nm']:
                zone = list()
                for i in self.args['NAME'].split(',') : 
                    zone.append(i.replace(" ", ""))       
            else :
                zone = sort.list_dns()
            vallist = sort.list_record(zone)
            print(tabulate(vallist))
            
            