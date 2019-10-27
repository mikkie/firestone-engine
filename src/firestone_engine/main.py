# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         firestone = firestone_engine.main:run

Then run `python setup.py install` which will install the command `firestone`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import ptvsd
import argparse
import sys
import time
import logging
from firestone_engine.DataLoader import DataLoader

from firestone_engine import __version__

__author__ = "aqua"
__copyright__ = "aqua"
__license__ = "mit"

_logger = logging.getLogger(__name__)

def get_data(codes):
    """get data from tushare

    Args:
      codes: list

    Returns:
      data
    """
    data_loader = DataLoader(codes)
    data_loader.start()
    try:
        while(not data_loader.is_finsih()):
            time.sleep(100)
    except KeyboardInterrupt:
        pass
    finally:
        data_loader.stop()


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="strategy engine for firestone")
    parser.add_argument(
        "--version",
        action="version",
        version="firestone-engine {ver}".format(ver=__version__))
    parser.add_argument(
        dest="codes",
        help="the stock codes, i.e. 300793 600213",
        nargs='+',
        metavar="code")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO)
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG)
    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        help="set to debug mode use vscode",
        action="store_true")        
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    if(args.debug):
        # 5678 is the default attach port in the VS Code debug configurations
        print("start debug on port 5678")
        ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
        ptvsd.wait_for_attach()
    setup_logging(args.loglevel)
    get_data(args.codes)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()

# # to debug in vscode uncomment this block
# import ptvsd
# # 5678 is the default attach port in the VS Code debug configurations
# print("start debug on port 5678")
# ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
# ptvsd.wait_for_attach()
