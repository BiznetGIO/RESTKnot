"""
Usage:
  dnsagent <command> [<args>...]

Options:
  -h, --help                             display this help and exit
  -v, --version                          Print version information and quit

Commands:
  zone            Zone Record Configuration Zone Command
  command         CZone onfiguration Command
  start           Starting Agent

Run 'dnsagent COMMAND --help' for more information on a command.
"""
import logging
import os
import sys
from inspect import getmembers, isclass
from logging.handlers import RotatingFileHandler

from docopt import docopt
import dnsagent.clis
from dnsagent import __version__ as VERSION


def configure_logger():
    log_path = os.environ.get("RESTKNOT_LOG_FILE")
    if not log_path:
        raise ValueError(f"RESTKNOT_LOG_FILE is not set")

    file_handler = RotatingFileHandler(log_path, maxBytes=1000000, backupCount=3)
    file_handler.setLevel(logging.WARNING)

    file_format = logging.Formatter(
        "[%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    )
    file_handler.setFormatter(file_format)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    stdout_handler.setFormatter(stdout_format)
    stdout_handler.setLevel(logging.INFO)

    root = logging.getLogger()
    root.addHandler(file_handler)
    root.addHandler(stdout_handler)
    root.setLevel(logging.DEBUG)


def main():
    """Main CLI entrypoint."""
    configure_logger()

    options = docopt(__doc__, version=VERSION, options_first=True)
    command_name = ""
    args = ""
    command_class = ""

    command_name = options.pop("<command>")
    args = options.pop("<args>")

    if args is None:
        args = {}

    try:
        module = getattr(dnsagent.clis, command_name)
        dnsagent.clis = getmembers(module, isclass)
        command_class = [
            command[1] for command in dnsagent.clis if command[0] != "Base"
        ][0]
    except AttributeError as e:
        raise ValueError(f"{e}")

    command = command_class(options, args)
    command.execute()


if __name__ == "__main__":
    main()
