"""
Usage:
  knot-cli <command> [<args>...]
  knot-cli -h | --help

Command :
  create      Create new DNS or Record
  rm          Remove owned DNS or Records
  ls          List all owned dns or records
  login       
  logout    

Run 'knot-cli <command> --help' for more information on a command.
"""

from inspect import getmembers, isclass
from docopt import docopt, DocoptExit


def main():
    """Main CLI entrypoint."""
    import clis
    options = docopt(__doc__, version='0.0.1', options_first=True)
    command_name = ""
    args = ""
    command_class =""

    command_name = options.pop('<command>')
    args = options.pop('<args>')

    if args is None:
        args = {}

    try:
        module = getattr(clis, command_name)
        clis = getmembers(module, isclass)
        command_class = [command[1] for command in clis
                   if command[0] != 'Base'][0]
    except AttributeError as e:
        print(e)
        raise DocoptExit()
    command = command_class(options, args)
    command.execute()
    


if __name__ == '__main__':
    main()
