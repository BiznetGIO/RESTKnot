from docopt import docopt

class Base(object):
    """Base class for the commands"""

    def __init__(self, options, command_args):
        """
        Initialize the commands.

        :param command_args: arguments of the command
        """
        self.options = options
        self.args = docopt(self.__doc__, argv=command_args)

    def execute(self):
        """Execute the commands"""
        raise NotImplementedError