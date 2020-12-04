#!/usr/bin/env -S python3
# -*- mode: python; flycheck-checker: python-flake8; -*-

"""Test Exceptions"""

import sys
import os
import io
import re
# from datetime import datetime
# from contextlib import suppress
# import traceback
import inspect
import argparse
# pip3 install justifytext
from justifytext import justify


def cls():
    """..."""
    os.system('cls' if os.name == 'nt' else 'clear')


def printDescribe(*args):
    """..."""
    printJustText(*args, maxch=76, prech=4)
    print()
    sys.exit(0)


def printJustText(*args, maxch=76, prech=4):
    """Print lines of text justified ..."""
    print()
    for aLine in args:
        x = justify(re.sub(r"^\s+|\s+$", "", aLine), maxch)
        if len(x) < 1:
            print()
        else:
            for i in x:
                print("%s%s" % (" " * prech, i))


def printEvalString(s):  # pylint: disable=missing-function-docstring
    print("%s=%s" % (s, eval(s)))  # pylint: disable=eval-used


def parseOptions():
    """Parse Options"""
    argsParser = argparse.ArgumentParser(description='Test Exception usage in Pyhton.')
    argsParser.add_argument('-e', '--describe', help="describe scope of this script.", default=False, action="store_true")
    return argsParser.parse_args()


def captureStdout(aClosure):
    """Test assign print output to a variable ..."""
    old_stdout = sys.stdout  # save stdout
    new_stdout = io.StringIO()  # create a string buffer (auto expand?)
    sys.stdout = new_stdout  # fake sys.stdout with a new output stream (io.StringIO())
    aClosure()
    outputString = new_stdout.getvalue()  # get content of io.StringIO()
    sys.stdout = old_stdout  # vedere anche: sys.__stdout__
    return outputString


# Using the special variable __name__
if __name__ == "__main__":
    # print("this file [%s] is a library" % inspect.currentframe().f_code.co_name, file=sys.stderr)
    print("this file [%s] is a library" % (inspect.stack()[0])[0].f_code.co_filename, file=sys.stderr)
else:
    pass
    # print("This only executes when %s is imported ..." % __file__)
    # print("this file [%s] was imported" % (inspect.stack()[0])[0].f_code.co_filename, file=sys.stderr)

# print("after __name__ guard")
