#!/usr/bin/env -S python3 -B
# -*- mode: python; flycheck-checker: python-flake8; -*-
# flake8: noqa
# noqa: E722,E305

"""Test: Colors (ANSI escape codes) ..."""

import os
import sys
from datetime import datetime

sys.path.append(os.path.expanduser("."))
sys.path.append(os.path.expanduser("../ansiesc_colors"))

import jj_funs as jf  # pylint: disable=unused-import,wrong-import-position,import-error  # noqa: F401,E402

from ansiesc_colors import co               # pylint: disable=wrong-import-position,unused-import,wrong-import-order
from ansiesc_colors import cf               # pylint: disable=wrong-import-position,unused-import,wrong-import-order
from ansiesc_colors import printColorTable  # pylint: disable=wrong-import-position,unused-import,wrong-import-order

scope = [
    """This is an example of colored string implementation in console using ANSI escape codes and written in Python.""",
]

esito = [
    """Example investigating how to using ANSI escape codes for colored text ...""",
]

def main():  # pylint: disable=missing-function-docstring,missing-class-docstring,bare-except  # noqa: E722,E305
    """Main entry"""

    parseArguments()

    initializeConsole(cls=True)

    printUndMessage("ANSI escape codes color tables")

    printColorTable()

    cf().test()

####################################################################################################

def parseArguments():  # pylint: disable=missing-function-docstring,missing-class-docstring,bare-except  # noqa: E722,E305
    args = jf.parseOptions()
    _ = jf.printDescribe(*scope) if args.describe else None

def printUndMessage(message):  # pylint: disable=missing-function-docstring,missing-class-docstring,bare-except  # noqa: E722,E305
    print("%s%s" % (" " * 4, message))
    print("%s%s" % (" " * 4, "-" * len(message)))

def initializeConsole(cls=True):  # pylint: disable=missing-function-docstring,missing-class-docstring,bare-except  # noqa: E722,E305
    print()
    if cls:
        jf.cls()  # clear console ... or also:  print(chr(27) + '[2j'),  print('\033c'), print('\x1bc')
    printUndMessage("Colors (ANSI escape codes) examples ... [%s]" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

def terminateConsole():  # pylint: disable=missing-function-docstring,missing-class-docstring,bare-except  # noqa: E722,E305
    jf.printJustText(*esito)
    print()

####################################################################################################

if __name__ == "__main__":
    main()
else:
    print("This only executes when %s is imported ..." % __file__)
