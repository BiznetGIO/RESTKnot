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
        ls record [(--nm-zone=ZNNAME [--nm-record=NAME] [--type=TYPE] )]
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
            if vallist['status'] == False:
                print(vallist['message'])
                exit()
            util.convert(vallist)
            vallist = vallist['data']
            show = list()
            for i in vallist:
                var = {"DNS NAME" : i}
                show.append(var)
            print('Your Domains List Are : ')
            
            print(tabulate(show,headers='keys',showindex='always',tablefmt="rst"))
        elif self.args['record'] :
            if self.args['--nm-zone']:
                id_record = list()
                zone = [self.args['--nm-zone']]
                tags = self.args
                vallist = ls.list_record(zone,tags)          
            else :
                zone = sort.list_dns()
                try:
                    zone = zone['data']
                    vallist = sort.list_record(zone)
                except Exception:
                    print(zone['message'])
                    exit()
            if vallist['status']:
                vallist = util.table_cleanup(vallist['data'])
                print(tabulate(vallist, headers="keys", showindex="always",tablefmt="rst"))
            else :
                print(vallist['message'])
                print("You have no record yet!")
            
            