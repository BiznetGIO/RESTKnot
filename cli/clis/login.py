import os
import getpass
from .base import Base
from libs import config as app
from libs import utils as util
from libs.wrapper import *

class Login(Base):
    """
    usage:
        login -n USERNAME

    Options :
    -n --username  USERNAME

    Commands:

    
    """
    
    def execute(self):
        pswd = getpass.getpass('Password : ')
        self.args['--pwd'] = pswd
