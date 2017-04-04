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
	
	
def extract_regex( values ):
	regex = ""
	regex_choices = []

	if isinstance( values, dict ):
		keys = values.keys()
	
		if len(keys):
			for key in keys:
				re_key = re.sub( r"([\?\[\]\(\)\.\{\}\;\+\*\^\$\-])", r"\\\1", re.sub( r"^'|'$", "", repr( key ) ) )
				regex_choices.append( re_key + extract_regex( values[key] ) )
		
			regex = "(%s)?" % "|".join( regex_choices )

	return regex


if __name__ == "__main__":
	keys = OrderedDict()
	keys["ENTER"] = '\n'
	keynames = [
		"ESCAPE",
		"TABULATION",
		"HOME",
		"END",
		"LEFT", "CTRL_LEFT",
		"RIGHT", "CTRL_RIGHT",
		"UP",
		"DOWN",
		"BACKSPACE",
		"DELETE" ]

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

	escape_characters = {}
	
	for key in keys:
		dest_dict = escape_characters
		
		for character in keys[key][:-1]:
			if character not in dest_dict:
				dest_dict[character] = {}
			
			dest_dict = dest_dict[character]
	
	escape_regex = "^%s$" % extract_regex( escape_characters )

	with open( "keys_%s.py" % SHELL_SYSTEM, "w" ) as f:
		f.write( "# -*- coding: utf-8 -*-\n\n" )
		
		f.write( "# Key escape regular expression\n" )
		f.write( "# While this expression matches, the key sequence is incomplete\n" )
		f.write( "escape_regex = b'%s'\n\n" % escape_regex )

		f.write( "# Registered keys\n" )
		for key in keys:
			f.write( "%s = %s\n" % (key, repr(keys[key])) )
	
