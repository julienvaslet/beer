#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import re
import os

from collections import OrderedDict

try:
	import termios
	import tty

	SHELL_SYSTEM = "unix"

# Windows case
except ImportError:
	import msvcrt
	SHELL_SYSTEM = "windows"


def getch():
    sequence = b""

    if SHELL_SYSTEM == "unix":
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        new_settings = termios.tcgetattr(fd)
        new_settings[3] = new_settings[3] & ~termios.ICANON & ~termios.ECHO
        new_settings[6][termios.VMIN] = 1
        new_settings[6][termios.VTIME] = 0

        termios.tcsetattr(fd, termios.TCSANOW, new_settings)
        escape_regex = re.compile(b'^(\xc2|\xc3|\x1b(O|\[([0-9]+(;([0-9]+)?)?)?)?)$')

        try:
            complete = False

            while not complete:
                sequence += os.read(fd, 1)

                if not escape_regex.match(sequence):
                    complete = True

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    # Windows case
    else:
        escape_regex = re.compile( b'^(\x00|\xe0)$' )
        complete = False

        while not complete:
            s = msvcrt.getch()

            if s == b'\r':
                s = b'\n'

            sequence += s

            if not escape_regex.match(sequence):
                complete = True

    return sequence


if __name__ == "__main__":
    keys = OrderedDict()
    keynames = [ "ENTER", "F1", "F2" ]

    for key in keynames:
        print( "Please type %s key (ENTER to skip): " % key, end="", flush=True )
        value = getch()

        try:
            value = value.decode( "utf-8", "replace" )

            if value == "\n" and key != "ENTER":
                print( "(skipping)" )
            else:
                print( value )
                keys[key] = value

        except UnicodeDecodeError:
            print( "\n[!] Unable to decode \"%s\" as UTF-8." % value )

    print( keys )
