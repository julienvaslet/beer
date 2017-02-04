# -*- coding: utf-8 -*-

import sys
import re

class Shell():

	def __init__( self, title="" ):
		self._title = title
		self._width = 80
		self._running = False
		self._verbosity = 1
		self._commands = {
			"help": {
				"description": "Shows this help message.",
				"function": self.help
			},
			"exit": {
				"description": "Exits the current shell.",
				"function": self.exit
			},
			"quit": { "alias": "exit" },
		}
		
		
	def error( self, message, code=0 ):
		if code > 0:
			message = "Error %d: %s" % ( code, message )
			
		print( "[!] %s" % message, file=sys.stderr )
		
		
	def log( self, message, level=1 ):
		if level <= self._verbosity:
			print( "[*] %s" % message )
			
			
	def exit( self, args=[] ):
		self.log( "Exiting" )
		self._running = False
	
	
	def help( self, args=[] ):
		print( "List of the available commands:\n" )
		
		commandNameLength = 0
		
		for command in self._commands:
			if "alias" not in self._commands[command]:
				if commandNameLength < len(command):
					commandNameLength = len(command)
	
		commandNameLength += 4
		
		for command in self._commands:
			if "alias" not in self._commands[command]:
				print( command.ljust( commandNameLength ), end="" )
				
				lines = 1
				
				# Print command description
				if "description" in self._commands[command]:
					i = 0
					lineLength = self._width - commandNameLength
					
					while i < len( self._commands[command]["description"] ):
						if i > 0:
							print( "".ljust( commandNameLength ), end="" )
							lines += 1
							
						print( self._commands[command]["description"][i:i+lineLength] )
						i += lineLength
						
				else:
					print( "No description available." )
					
				# Look for command aliases
				aliases = []
				
				for alias in self._commands:
					if "alias" in self._commands[alias] and self._commands[alias]["alias"] == command:
						aliases.append( alias )
				
				# Print aliases' list if any
				# WARN: if alias name is larger than shell width -> infinite loop
				if len(aliases):
					aliasTitle = "Aliases:"
					lineLength = self._width - commandNameLength - len(aliasTitle)
					
					print( "%s%s" % ( "".ljust( commandNameLength ), aliasTitle ), end="" )
					
					aliasLine = ""
					
					for alias in aliases:
						if len(aliasLine) + len(alias) + 1 > lineLength:
							print( aliasLine )
							aliasLine = "".ljust( commandNameLength + len(aliasTitle) )
							lines += 1
							
						aliasLine += " %s," % alias
					
					print( aliasLine[:len(aliasLine)-1] )
					lines += 1
				
				# If the command's information is larger than 1 line, empty line is added
				if lines > 1:
					print( "" )
				
				
	def run( self, args=[] ):
		self._running = True
		separatorPattern = re.compile( '\s+' )
		
		while self._running:
			try:
				# history navigation: start a thread that look for UP, DOWN, TAB keys
				print( self._title, end=' > ' )
				commandline = input()
				command = None
			
				args = list( filter( len, separatorPattern.split( commandline.strip() ) ) )

				if len( args ) == 0:
					continue
			
				if args[0] in self._commands:
					command = args[0]
					
					if "alias" in self._commands[command]:
						if self._commands[command]["alias"] in self._commands:
							command = self._commands[command]["alias"]
						else:
							self.error( "Referenced command \"%s\" not found for alias \"%s\"." % (command, self._commands[command]["alias"]) )
							command = None
						
					if "function" not in self._commands[command] or not callable( self._commands[command]["function"] ):
						self.error( "Command \"%s\" is not executable." % command )
						command = None
					
				if command != None:
					self._commands[command]["function"]( args )
				else:
					self.error( "Unknown command %s." % args[0] )
					
			except KeyboardInterrupt:
				print()
				self.log( "Interrupted by user.", level=0 )
				self.exit()
	
