#!/usr/bin/env -S python3 -B
# -*- flycheck-checker: python-flake8; -*-
# flake8: noqa
# noqa: E722,E305

""" Colors (ANSI escape codes) ... """

import subprocess
import threading
import shlex
import re


def main():
    """Main entry"""

    printColorTable()

    cf().test()

### some module private variables, starts here ###

_esc_ = '\033'  # Escape code (ANSI Escape Codes) prefix
_csi_ = _esc_ + "["  # Control Sequence Introducer (ANSI Escape Codes)
_ncolors_ = int(subprocess.run(shlex.split("/usr/bin/tput colors 2>/dev/null"), stdout=subprocess.PIPE, check=True, shell=False).stdout.decode('utf-8'))
_ac_ = {key: "%s38;5;%dm" % (_csi_, key) for key in range(256)}  # text colors
_ab_ = {key: "%s48;5;%dm" % (_csi_, key) for key in range(256)}  # text on background colors

_acl_ = len(_ac_)
_abl_ = len(_ab_)

# attention: 'standout' is not usable because it needs the execution of the tput program before issuing the string ...
_color_qualifiers_ = {       "normal": f"{_csi_}0m",      "reset": f"{_csi_}0m",
                               "bold": f"{_csi_}1m",      "faint": f"{_csi_}2m",      "italic": f"{_csi_}3m",
                          "underline": f"{_csi_}4m",      "blink": f"{_csi_}5m",     "reverse": f"{_csi_}7m",
                       "underlineoff": f"{_csi_}24m",  "blinkoff": f"{_csi_}25m", "reverseoff": f"{_csi_}27m",
                              "font0": f"{_csi_}10m",     "font1": f"{_csi_}11m",      "font2": f"{_csi_}12m",
                              "font3": f"{_csi_}13m",     "font4": f"{_csi_}14m",      "font5": f"{_csi_}15m",
                              "font6": f"{_csi_}16m",     "font7": f"{_csi_}17m",      "font8": f"{_csi_}18m",
                              "font9": f"{_csi_}19m",  "standout": "$(tput smso  2>/dev/null)",
                             "framed": f"{_csi_}51m", "encircled": f"{_csi_}52m", }

# color names ...
_color_names_ = ( "black", "maroon", "green", "olive",  "navy", "purple",  "teal", "silver",
                  "gray",  "red",    "lime",  "yellow", "blue", "magenta", "cyan", "white" )

# background color names ...
_background_color_names_ = ( "bblack", "bmaroon", "bgreen", "bolive",  "bnavy", "bpurple",  "bteal", "bsilver",
                             "bgray",  "bred",    "blime",  "byellow", "bblue", "bmagenta", "bcyan", "bwhite" )

_fcnl_ = len(_color_names_)
_bcnl_ = len(_background_color_names_)

_cn_ = {_color_names_[key]: "%s" % (_ac_[key]) for key in range(len(_color_names_))}  # color ansi escape string by name
_bn_ = {_background_color_names_[key]: "%s" % (_ab_[key]) for key in range(len(_background_color_names_))}  # background color ansi escape string by name
_an_ = {'blu': _cn_['blue'],   'brown':  _cn_['maroon'] }  # alias of color ansi escape string by name
_dn_ = {'bblu': _bn_['bblue'], 'bbrown': _bn_['bmaroon']}  # alias of color ansi escape string by name

### some module private variables, ends here  ###


class _co:  # pylint: disable=too-many-instance-attributes,line-too-long,missing-function-docstring,no-self-use

    """color class (private to module) co will a singleton instance ..."""

    __instance = None

    @staticmethod
    def getInstance(data="", force=True):
        """double locking singleton"""

        if _co.__instance is None:
            with threading.Lock():
                if _co.__instance is None:
                    _co(data, force)  # see first lines of __init__ where it sets _co .__ instance
        return _co.__instance

    def __init__(self, data="", force=True):  # pylint: disable=line-too-long

        # see at getInstance method
        if _co.__instance is not None:
            raise Exception("This is A Singleton Class")
        _co.__instance = self

        self._force = force
        self._aaaa = ""
        self._zzzz = ""
        self._data = data

        _ = [ setattr(self, key, val) for key, val in _color_qualifiers_.items() ] if self._forceP() else ""
        _ = [ setattr(self, key, val) for key, val in _cn_.items() ] if self._forceP() else ""
        _ = [ setattr(self, key, val) for key, val in _bn_.items() ] if self._forceP() else ""
        _ = [ setattr(self, key, val) for key, val in _an_.items() ] if self._forceP() else ""
        _ = [ setattr(self, key, val) for key, val in _dn_.items() ] if self._forceP() else ""
        _ = [ setattr(self, "c%s" % key, val) for key, val in _ac_.items() ] if self._forceP() else ""
        _ = [ setattr(self, "b%s" % key, val) for key, val in _ab_.items() ] if self._forceP() else ""

    def __getattr__(self, item):
        return ""

    def __call__(self, data, *args):
        self._aaaa = ""
        self._zzzz = ""
        self._data = data
        if not self._forceP():
            # no colors available
            return self._data
        # prefix mode
        bAppend = False
        largs = list(args)
        while len(largs) > 0:
            if isinstance(largs[0], int):
                # color number {fore,back}ground
                if largs[0] < 0:
                    # background color
                    if bAppend:
                        self._zzzz = self._zzzz + _ab_.get((1 - largs[0]) % _abl_, "")  # default useless
                    else:
                        self._aaaa = self._aaaa + _ab_.get((1 - largs[0]) % _abl_, "")  # default useless
                else:
                    # foreground color
                    if bAppend:
                        self._zzzz = self._zzzz + _ac_.get(largs[0] % _acl_, "")  # default useless
                    else:
                        self._aaaa = self._aaaa + _ac_.get(largs[0] % _acl_, "")  # default useless
            elif isinstance(largs[0], str):
                # ANSI escape code string
                if bAppend:
                    self._zzzz = self._zzzz + largs[0]
                else:
                    self._aaaa = self._aaaa + largs[0]
            else:
                # switch to append mode
                bAppend = True
            largs.pop(0)
        return self._aaaa + self._data + self._zzzz

    def _forceP(self):
        """force predicate ..."""
        return _ncolors_ > 0 or self._force

    def ncolors(self):
        """Inferred number of colors using tput utility"""
        return _ncolors_

    def csi(self):
        """Control Sequence Introducer (ANSI Escape Codes)"""
        return  _csi_

    def ac(self):
        """Foreground colors (ANSI Escape Codes string)"""
        return _ac_

    def ab(self):
        """Background colors (ANSI Escape Codes string)"""
        return _ab_

    def color_qualifiers(self):
        """Color qualifires (ANSI Escape Codes string)"""
        return _color_qualifiers_

    def color_names(self):
        """Color names (Tuple)"""
        return _color_names_

    def background_color_names(self):
        """Background color names (Tuple)"""
        return _background_color_names_

    def cn(self):
        """Foreground colors (Dictionary) by name (ANSI Escape Codes string)"""
        return _cn_

    def bn(self):
        """Background colors (Dictionary) by name (ANSI Escape Codes string)"""
        return _bn_

    def an(self):
        """Foreground colors aliases (Dictionary) by name (ANSI Escape Codes string)"""
        return _an_

    def dn(self):
        """Background colors aliases (Dictionary) by name (ANSI Escape Codes string)"""
        return _dn_


class cf:  # pylint: disable=too-many-instance-attributes,line-too-long,missing-function-docstring,no-self-use

    """color class (private to module) --> co singleton instance ..."""

    def __init__(self, data="", force=True):  # pylint: disable=line-too-long

        self._data = data
        self._force = force

        self._hhhh = ""
        self._tttt = ""
        self._rrrr = ""
        self._data = data

        _ = [ setattr(self, key, val) for key, val in _color_qualifiers_.items() ] if self._forceP() else ""
        _ = [ setattr(self, key, val) for key, val in _cn_.items() ] if self._forceP() else ""
        _ = [ setattr(self, key, val) for key, val in _bn_.items() ] if self._forceP() else ""
        _ = [ setattr(self, key, val) for key, val in _an_.items() ] if self._forceP() else ""
        _ = [ setattr(self, key, val) for key, val in _dn_.items() ] if self._forceP() else ""
        _ = [ setattr(self, "c%s" % key, val) for key, val in _ac_.items() ] if self._forceP() else ""
        _ = [ setattr(self, "b%s" % key, val) for key, val in _ab_.items() ] if self._forceP() else ""

    def test(self):
        """test"""

        print(cf(" " * 4).h(co.normal)
              .a("test in bold blue ......").h(co.normal).h(co.blue).h(co.bold).t(co.normal)
              .a(" and in bold red ....").h(co.normal).h(co.red).h(co.bold).t(co.normal)
              .r())

        cfi = cf()
        print( cfi.a(" " * 4).h(co.normal)
               .a("test in bold magenta ...").h(cfi.normal).h(cfi.magenta).h(cfi.bold).t(cfi.normal)
               .a(" and in bold lime ...").h(cfi.normal).h(cfi.lime).h(cfi.bold).t(cfi.normal)
               .r())

    def h(self, data):
        """add data to head ..."""
        if not self._forceP():
            # no colors available
            return self
        self._hhhh = self._hhhh + data
        return self

    def t(self, data):
        """add data to tail ..."""
        if not self._forceP():
            # no colors available
            return self
        self._tttt = self._tttt + data
        return self

    def a(self, data=""):
        """restart data ..."""
        self._rrrr = self._rrrr + self._hhhh + self._data + self._tttt
        self._hhhh = ""
        self._tttt = ""
        self._data = data
        return self

    def r(self):
        """return data, reduce to data ..."""
        self.a()
        return self._rrrr

    def _forceP(self):
        """force predicate ..."""
        return _ncolors_ > 0 or self._force

    @classmethod
    def ncolors(cls):
        """Inferred number of colors using tput utility"""
        return _ncolors_

    @classmethod
    def csi(cls):
        """Control Sequence Introducer (ANSI Escape Codes)"""
        return  _csi_

    @classmethod
    def ac(cls):
        """Foreground colors (ANSI Escape Codes string)"""
        return _ac_

    @classmethod
    def ab(cls):
        """Background colors (ANSI Escape Codes string)"""
        return _ab_

    @classmethod
    def color_qualifiers(cls):
        """Color qualifires (ANSI Escape Codes string)"""
        return _color_qualifiers_

    @classmethod
    def color_names(cls):
        """Color names (Tuple)"""
        return _color_names_

    @classmethod
    def background_color_names(cls):
        """Background color names (Tuple)"""
        return _background_color_names_

    @classmethod
    def cn(cls):
        """Foreground colors (Dictionary) by name (ANSI Escape Codes string)"""
        return _cn_

    @classmethod
    def bn(cls):
        """Background colors (Dictionary) by name (ANSI Escape Codes string)"""
        return _bn_

    @classmethod
    def an(cls):
        """Foreground colors aliases (Dictionary) by name (ANSI Escape Codes string)"""
        return _an_

    @classmethod
    def dn(cls):
        """Background colors aliases (Dictionary) by name (ANSI Escape Codes string)"""
        return _dn_


def _printColorTable():  # pylint: disable=too-many-instance-attributes,line-too-long,missing-function-docstring,redefined-outer-name
    """Print the Color Table"""

    ss = " " * 4
    rv = getattr(co, "reverse")
    no = getattr(co, "normal")

    title = " standard and high intesity color names "
    print(co(ss, co.normal) + co(title + " " * (117 - len(title)), co.normal, co.faint, co.italic, co.reverse, None, co.normal))
    i = 0
    for a in list(co.cn()):
        _ = ( ( i % 4 ) ==  0 ) and print(co(" ", co.normal), end="")
        sa = getattr(co, f"{a}")
        print("%s   %3d %s%s   %s %s%-9s" % (no, i, sa, rv, no, no, a ), end="")
        i += 1
        _ = ( ( i % 4 ) ==  0 ) and print(co("", co.normal))
    _ = ( ( i % 4 ) !=  0 ) and print(co("", co.normal))

    title = " set color and reverse it (standard and high intesity) "
    print(co(ss, co.normal) + co(title + " " * (117 - len(title)), co.normal, co.faint, co.italic, co.reverse, None, co.normal))
    for i in range(len(co.cn())):
        _ = ( ( i % 8 ) ==  0 ) and print(co(" ", co.normal), end="")
        c0 = co.ac()[i]
        print("%s   %3d %s%s   %s" % (no, i, c0, rv, no ), end="")
        i += 1
        _ = ( ( i % 8 ) ==  0 ) and print(co("", co.normal))
    _ = ( ( i % 8 ) !=  0 ) and print(co("", co.normal))

    title = " set backgroung color (standard and high intesity) "
    print(co(ss, co.normal) + co(title + " " * (117 - len(title)), co.normal, co.faint, co.italic, co.reverse, None, co.normal))
    for i in range(len(co.cn())):
        _ = ( ( i % 8 ) ==  0 ) and print(co(" ", co.normal), end="")
        c0 = co.ab()[i]
        print("%s   %3d %s   %s" % (no, i, c0, no ), end="")
        i += 1
        _ = ( ( i % 8 ) ==  0 ) and print(co("", co.normal))
    _ = ( ( i % 8 ) !=  0 ) and print(co("", co.normal))

    title = " 16-231:  6 × 6 × 6 cube (216 colors): 16 + 36 × r + 6 × g + b (0 ≤ r, g, b ≤ 5) "
    print(co(ss, co.normal) + co(title + " " * (117 - len(title)), co.normal, co.faint, co.italic, co.reverse, None, co.normal))
    for i in range(16, 231+1, 1):
        _ = ( ( ( i - 16 ) % 12 ) ==  0 ) and print(co(" ", co.normal), end="")
        c0 = co.ac()[i]
        print("%s   %3d %s%s   %s" % (no, i, c0, rv, no ), end="")
        i += 1
        _ = ( ( ( i - 16 ) % 12 ) ==  0 ) and print(co("", co.normal))
    _ = ( ( ( i - 16 ) % 12 ) !=  0 ) and print(co("", co.normal))

    title = " 232-255:  grayscale from black to white in 24 steps "
    print(co(ss, co.normal) + co(title + " " * (117 - len(title)), co.normal, co.faint, co.italic, co.reverse, None, co.normal))
    for i in range(232, 255+1, 1):
        _ = ( ( ( i - 232 ) % 12 ) ==  0 ) and print(co(" ", co.normal), end="")
        c0 = co.ac()[i]
        print("%s   %3d %s%s   %s" % (no, i, c0, rv, no ), end="")
        i += 1
        _ = ( ( ( i - 232 ) % 12 ) ==  0 ) and print(co("", co.normal))
    _ = ( ( ( i - 232 ) % 12 ) !=  0 ) and print(co("", co.normal))

    print(co("", co.normal))
    print(ss + co("sample message (italic, color 208)", co.normal, 208, co.italic, None, co.normal))

def _test():  # pylint: disable=too-many-instance-attributes,line-too-long,missing-function-docstring,redefined-outer-name
    print("test")

co = _co.getInstance(force=False)

printColorTable = lambda: _printColorTable()  # pylint: disable=unnecessary-lambda

# https://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
# /(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]/ 
reAnsiEscapeSequence = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')

def stripAnsiEscSeq(data):  # pylint: disable=missing-function-docstring
    """remove escape ansi sequencces"""
    if not isinstance(data, str):
        return data
    return reAnsiEscapeSequence.sub('', data)

# Using the special variable __name__
if __name__ == "__main__":
    main()
else:
    pass

# In Python, "privacy" depends on  "consenting adults'" levels of agreement - you can't force it  (any more than you can
# in real life;-).  A single leading underscore means you're not supposed to access it "from the outside" -- two leading
# underscores (w/o trailing underscores) carry the message even more  forcefully... but, in the end, it still depends on
# social  convention and  consensus: Python's  introspection is  forceful  enough that  you can't  handcuff every  other
# programmer in the world to respect your wishes.

# No variable of  a module is really  private. However, by convention,  starting an identifier with  a single underscore
# (_), such as  _secret, indicates that the identifier is  meant to be private.  In other  words, the leading underscore
# communicates to client-code programmers that they should  not access the identifier directly. Development environments
# and other tools  rely on the leading-underscore naming convention  to discern which attributes of a  module are public
# (i.e., part of  the module's interface) and which  ones are private (i.e., to  be used only within the  module). It is
# good programming practice  to distinguish between private and  public attributes by starting the private  ones with _,
# for clarity and  to get maximum benefit  from tools. It is particularly  important to respect the  convention when you
# write client  code that uses modules  written by others.  In other words, avoid  using any attributes in  such modules
# whose names start with _. Future releases of the modules  will no doubt maintain their public interface, but are quite
# likely to change private implementation details.
