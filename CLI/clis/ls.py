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
            util.convert(vallist)
            show = list()
            for i in vallist:
                var = {"DNS NAME" : i}
                show.append(var)
            print('Your Domains List Are : ')
            
            print(tabulate(show,headers='keys',showindex='always',tablefmt="rst"))
        elif self.args['record'] :
            if self.args['--nm']:
                zone = list()
                for i in self.args['NAME'].split(',') : 
                    zone.append(i.replace(" ", ""))       
            else :
                zone = sort.list_dns()
            vallist = sort.list_record(zone)
            if vallist:
                vallist = util.table_cleanup(vallist)
                print(tabulate(vallist, headers="keys", showindex="always",tablefmt="rst"))
            else :
                print("You have no record yet!")
            
            