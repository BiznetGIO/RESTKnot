import os
import sys
from .base import Base
from libs import utils as util
from libs import config as app
from libs import listing as sort
from libs.wrapper import *
import string
from tabulate import tabulate

class Ls(Base):
    """
    Usage:
        ls ttl
        ls type
        ls record [(--nm-zone=ZNNAME [--nm-record=NAME] [--type=TYPE] )]
        ls dns
        ls -h | --help

    Options :
    
    --nm-zone ZNNAME            Filter by zone's name
    --nm-record NAME            Filter by record's name
    --type TYPE                 Filter by record's type
    -h --help                   Print usage and helps
    
    Commands:
     ttl                        List available ttl
     type                       List available type 
     record                     List available record
     zone                       List available zone

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
            d_dns = list()
            for row in vallist:
                state = sort.get_data("zone","state","nm_zone",row)
                state = state["data"][0]
                d_dns.append({"nm_zone" : row, "state" : state})
            print('Your Domains List Are : ')
            
            print(tabulate(d_dns,headers='keys',showindex='always',tablefmt="rst"))
        elif self.args['record'] :
            if self.args['--nm-zone']:
                zone = [self.args['--nm-zone']]
                tags = self.args
                vallist = ls.list_record(zone,tags)          
            else :
                zone = sort.list_dns()
                try:
                    zone = zone['data']
                    vallist = sort.list_record(zone)
                except Exception:
                    sys.stderr.write(zone['message']+'\n')
                    exit()
            if vallist['status'] and 'data' in vallist:
                vallist = util.table_cleanup(vallist['data'])
                print(tabulate(vallist, headers="keys", showindex="always",tablefmt="rst"))
            else :
                
                print("You have no record yet.")
            
            