import os
from .base import Base
from libs import utils as util
from libs import config as app
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
            vallist = app.listing_endpoint('ttl')
            print('Available ttl values are : ')
            print(vallist)
        elif self.args['type']:
            vallist = app.listing_endpoint('type')
            print('Available type values are : ')
            print(vallist)