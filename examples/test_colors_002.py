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
from ansiesc_colors import stripAnsiEscSeq  # pylint: disable=wrong-import-position,unused-import,wrong-import-order

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

    printUndMsg("Some other examples ...")

    printMsg("_ncolors_=%d" % co.ncolors())

    printMsg(co("", co.normal))
    printMsg(co("--- test with blue ---", co.normal))

    printMsg(co(" blue ", co.normal, co.blue, co, co.normal))
    printMsg(co(" blue and bold ", co.normal, co.blue, co.bold, co, co.normal))
    printMsg(co(" blue and bold and reverse ", co.normal, co.blue, co.bold, co.reverse, co, co.normal))
    printMsg(co(" white on blue ", co.normal, co.c255, co.b12, co, co.normal))
    printMsg(co(" white on blue and bold ", co.normal, co.c255, co.b12, co.bold, co, co.normal))
    printMsg(co(" white on blue and italic ", co.normal, co.c255, co.b12, co.italic, co, co.normal))

    printMsg(co("", co.normal))
    printMsg(co("--- another test with red ---", co.normal))

    printMsg(cf().a(" red ").h(co.normal).h(co.red).t(co.normal).r())
    printMsg(cf().a(" red and bold ").h(co.normal).h(co.red).h(co.bold).t(co.normal).r())
    printMsg(cf().a(" red and bold and reverse ").h(co.normal).h(co.red).h(co.bold).h(co.reverse).t(co.normal).r())
    printMsg(cf().a(" white on red ").h(co.normal).h(co.c255).h(co.b9).t(co.normal).r())
    printMsg(cf().a(" white on red and bold ").h(co.normal).h(co.c255).h(co.b9).h(co.bold).t(co.normal).r())
    printMsg(cf().a(" white on red and italic ").h(co.normal).h(co.c255).h(co.b9).h(co.italic).t(co.normal).r())

    printMsg(co("", co.normal))
    printMsg(co("--- another test ---", co.normal))

    printMsg(cf(" " * 0).h(co.normal)
          .a("test in bold blue ......").h(co.normal).h(co.blue).h(co.bold).t(co.normal)
          .a(" and in reverse bold red ....").h(co.normal).h(co.red).h(co.bold).h(co.reverse).t(co.normal)
          .r())

    printMsg(co("", co.normal))
    printMsg(co("--- Test strip ANSI escape sequences ---", co.normal))

    coloredString = (cf(" " * 0).h(co.normal).a("test strip ANSI Escape Sequences ... ")
                     .a("test in bold blue ......").h(co.normal).h(co.blue).h(co.bold).t(co.normal)
                     .a(" and in reverse bold red ....").h(co.normal).h(co.red).h(co.bold).h(co.reverse).t(co.normal)
                     .r())

    printMsg(coloredString)

    printMsg(stripAnsiEscSeq(coloredString))

    printMsg(co("", co.normal))
    printMsg(co("--- Messages, Warnings and Errors ---", co.normal))

    escMessage = cf().h(co.normal).h(co.cyan).h(co.bold).h(co.italic).r()
    escWarning = cf().h(co.normal).h(co.yellow).h(co.bold).h(co.italic).r()
    escError   = cf().h(co.normal).h(co.red).h(co.bold).h(co.italic).r()
    printMsg(cf(" " * 0).h(escMessage).a("MESSAGE: message sample").t(co.normal).r())
    printMsg(cf(" " * 0).h(escWarning).a("WARNING: warning sample").t(co.normal).r())
    printMsg(cf(" " * 0).h(escError).a("ERROR:   error sample").t(co.normal).r())
    printMsg(cf("MESSAGE: message sample again ...").h(escMessage).t(co.normal).r())
    printMsg(cf("WARNING: warning sample again ...").h(escWarning).t(co.normal).r())
    printMsg(cf("ERROR:   error   sample again ...").h(escError).t(co.normal).r())

####################################################################################################

def parseArguments():  # pylint: disable=missing-function-docstring,missing-class-docstring,bare-except  # noqa: E722,E305
    args = jf.parseOptions()
    _ = jf.printDescribe(*scope) if args.describe else None

def printMsg(message, *args, **kargs):  # pylint: disable=missing-function-docstring,missing-class-docstring,bare-except  # noqa: E722,E305
    print("%s%s" % (" " * 4, message), *args, **kargs)

def printUndMsg(message, *args, **kargs):  # pylint: disable=missing-function-docstring,missing-class-docstring,bare-except  # noqa: E722,E305
    print("%s%s" % (" " * 4, message), *args, **kargs)
    print("%s%s" % (" " * 4, "-" * len(message)))

def initializeConsole(cls=True):  # pylint: disable=missing-function-docstring,missing-class-docstring,bare-except  # noqa: E722,E305
    print()
    if cls:
        jf.cls()  # clear console ... or also:  print(chr(27) + '[2j'),  print('\033c'), print('\x1bc')
    printUndMsg("Colors (ANSI escape codes) examples ... [%s]" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

def terminateConsole():  # pylint: disable=missing-function-docstring,missing-class-docstring,bare-except  # noqa: E722,E305
    jf.printJustText(*esito)
    print()

####################################################################################################

if __name__ == "__main__":
    main()
else:
    print("This only executes when %s is imported ..." % __file__)
