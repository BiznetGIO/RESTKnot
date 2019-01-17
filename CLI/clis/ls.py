import os
from .base import Base
from libs import utils as util
from libs import config as app
from libs import ls
from libs.wrapper import *

class Ls(Base):
    """
    usage:
        ls ttl
        ls type
        ls record
        ls dns

    Options :
   

    Commands:
     ttl                        List available ttl
     type                       List available type 
    
    """
    @login_required
    def execute(self):
        if self.args['ttl'] :
            vallist = ls.listing_endpoint('ttl')
            print('Available ttl values are : ')
            print(vallist)
        elif self.args['type']:
            vallist = ls.listing_endpoint('type')
            print('Available type values are : ')
            print(vallist)
        elif self.args['dns']:
            vallist = ls.list_dns()
            print('Your Domains List Are : ')
            print(vallist)