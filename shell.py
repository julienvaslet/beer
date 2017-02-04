# -*- coding: utf-8 -*-

import sys
import re

class Shell():

	def __init__( self, title="" ):
		self._title = title
		self._running = False
		self._verbosity = 1
		self._commands = {
			"exit": self.exit,
			"quit": self.exit
		}
		
		
	def error( self, message, code=0 ):
		if code > 0:
			message = "Error %d: %s" % ( code, message )
			
		print( "[!] %s" % message, file=sys.stderr )
		
		
	def log( self, message, level=1 ):
		if level <= self._verbosity:
			print( "[*] %s" % message )
			
			
	def exit( self ):
		self.log( "Exiting" )
		self._running = False
	
	
	def run( self ):
		self._running = True
		separatorPattern = re.compile( '\s+' )
		
		while self._running:
			try:
				# history navigation: start a thread that look for UP, DOWN, TAB keys
				print( self._title, end=' > ' )
				commandline = input()
			
				args = list( filter( len, separatorPattern.split( commandline.strip() ) ) )

				if len( args ) == 0:
					continue
			
				if args[0] in self._commands:
					self._commands[args[0]]()
				else:
					self.error( "Unknown command %s." % args[0] )
					
			except KeyboardInterrupt:
				print()
				self.log( "Interrupted by user.", level=0 )
				self.exit()
	
