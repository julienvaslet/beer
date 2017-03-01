# -*- coding: utf-8 -*-

current_shell = None
verbosity = 1

# Verbosities are:
#	- 0: quiet
#	- 1: normal
#	- 2: user debug
#	- 3: development debug

def info( message, level=1 ):
	global current_shell
	global verbosity
	
	if current_shell == None:
		if verbosity >= level:
			print( "[*] %s" % message )
	else:
		current_shell.log( message, level=level )
		

def debug( message ):
	global current_shell
	global verbosity
	
	if current_shell == None:
		if verbosity >= 3:
			print( "[*] %s" % message )
	else:
		current_shell.log( message, level=3 )
		

def warn( message, level=1 ):
	global current_shell
	global verbosity
	
	if current_shell == None:
		if verbosity >= level:
			print( "[!] %s" % message )
	else:
		current_shell.warn( message, level=level )
		

def error( message ):	
	global current_shell
	
	if current_shell == None:
		print( "[!] %s" % message, file=sys.stderr )
	else:
		current_shell.error( message )

