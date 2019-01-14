import os
import sys
from .base import Base
from libs import utils as util
from libs import config as app

class Rm(Base):
    """
    usage:
        rm dns (--nm NAME)
        rm record (--nm-record NAME )

    Options :
        -h --help               Print usage
        --nm  NAME        DNS/Record's name to delete

    Commands:
     ttl                        List available ttl
     type                       List available type 
    
    """
    def execute(self):
        if self.args['dns']:

            #FILTER DIDIEU 
            app.remove_data(self.args['--nm'],'zone')

        elif self.args['record']:

            app.remove_data(self.args['--nm'],'record')