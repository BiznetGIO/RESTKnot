
import os
import getpass
from .base import Base
from libs.auth import ex_logout
from libs import config as app
from libs import utils as util
from libs.wrapper import *

class Login(Base):
    """
    usage:
        logout [-r]

    Options :
        -r          Delete Cache for Fresh Login


    Commands:

    """

    def execute(self):
        ex_logout(self.args['-r'])
        
