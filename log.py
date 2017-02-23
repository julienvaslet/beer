# -*- coding: utf-8 -*-

currentShell = None
verbosity = 1

# Verbosities are:
#	- 0: quiet
#	- 1: normal
#	- 2: user debug
#	- 3: development debug

def info( message, level=1 ):
	global currentShell
	global verbosity
	
	if currentShell == None:
		if verbosity >= level:
			print( "[*] %s" % message )
	else:
		currentShell.log( message, level=level )
		

def debug( message ):
	global currentShell
	global verbosity
	
	if currentShell == None:
		if verbosity >= 3:
			print( "[*] %s" % message )
	else:
		currentShell.log( message, level=3 )
		

def warn( message, level=1 ):
	global currentShell
	global verbosity
	
	if currentShell == None:
		if verbosity >= level:
			print( "[!] %s" % message )
	else:
		currentShell.warn( message, level=level )
		

def error( message ):	
	global currentShell
	
	if currentShell == None:
		print( "[!] %s" % message, file=sys.stderr )
	else:
		currentShell.error( message )

