#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import re
import os
import fcntl

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
		new_settings[6][termios.VMIN] = 0
		new_settings[6][termios.VTIME] = 0

		termios.tcsetattr( fd, termios.TCSANOW, new_settings )
		
		# Non-block input
		flag = fcntl.fcntl( fd, fcntl.F_GETFL )
		fcntl.fcntl( fd, fcntl.F_SETFL, flag | os.O_NONBLOCK )

		try:
			while len(sequence) == 0:
				ch = os.read( fd, 1 )
				
				while ch != None and len(ch) > 0:
					sequence += ch
					ch = os.read( fd, 1 )

		finally:
			termios.tcsetattr(fd, termios.TCSANOW, old_settings)
			fcntl.fcntl( fd, fcntl.F_SETFL, flag )

	# Windows case
	else:
		while len(sequence) == 0:
			while msvcrt.kbhit():
				s = msvcrt.getch()

				if s == b'\r':
					s = b'\n'

				sequence += s

	return sequence


if __name__ == "__main__":
	keys = OrderedDict()
	keys["ENTER"] = '\n'
	keynames = [ "ESCAPE", "F1", "F2" ] #, "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "INSERT", "DELETE" ]

	for key in keynames:
		print( "Please type %s key (ENTER to skip): " % key, end="", flush=True )
		value = getch()

		try:
			value = value.decode( "utf-8", "replace" )

			if value == "\n":
				print( "(skipped)" )
				keys[key] = None
			else:
				print( repr(value) )
				keys[key] = value

		except UnicodeDecodeError:
			print( "\n[!] Unable to decode \"%s\" as UTF-8." % repr(value) )

	with open( "keys_%s.py" % SHELL_SYSTEM, "w" ) as f:
		f.write( "# -*- coding: utf-8 -*-\n\n" )

		for key in keys:
			f.write( "%s = %s\n" % (key, repr(keys[key])) )
	
