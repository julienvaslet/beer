# -*- coding: utf-8 -*-

import sys
import re
import os
import tty
import termios

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
			"quit": { "alias": "exit" }
		}
		
		
	def error( self, message, code=0 ):
		if code > 0:
			message = "Error %d: %s" % ( code, message )
			
		print( "[!] %s" % message, file=sys.stderr )
		
		
	def log( self, message, level=1 ):
		if level <= self._verbosity:
			self.print( message, leftText="[*]", lpad=4 )
			
			
	def exit( self, args=[] ):
		self._running = False
	
	
	def getch( self ):
		character = None

		fd = sys.stdin.fileno()
		oldSettings = termios.tcgetattr( fd )
		newSettings = termios.tcgetattr( fd )
		newSettings[3] = newSettings[3] & ~termios.ICANON & ~termios.ECHO
		newSettings[6][termios.VMIN] = 1
		newSettings[6][termios.VTIME] = 0

		termios.tcsetattr( fd, termios.TCSANOW, newSettings )

		try:
			character = os.read( fd, 4 )

		finally:
			termios.tcsetattr( fd, termios.TCSADRAIN, oldSettings )

		return character


	def input( self, prompt="" ):
		
		if len( prompt ):
			os.write( sys.stdout.fileno(), prompt.encode( "ASCII" ) )
		
		line = ""
		lineIndex = 0
		lastLineIndex = 0
		lineRead = False
		
		while not lineRead:
			rawkey = self.getch()
			rewriteLine = False
			
			try:
				key = rawkey.decode( "utf-8" )
				
			except UnicodeDecodeError:
				continue
			
			# End of line
			if key == "\x0a":
				lineRead = True
			
			# Tabulation
			#elif key == "\x09":
			#	print( "TAAABS" )
				
			# Up
			#elif key == "\x1b[A":
			#	print( "UUUUP" )
				
			# Down
			#elif key == "\x1b[B":
			#	print( "DOOOWN" )
			
			# Left
			elif key == "\x1b[D":
			
				if lineIndex > 0:
					lineIndex -= 1
					rewriteLine = True
				
				else:
					os.write( sys.stdout.fileno(), b'\x07' )
			
			# Right
			elif key == "\x1b[C":
			
				if lineIndex < len(line):
					lineIndex += 1
					rewriteLine = True
				
				else:
					os.write( sys.stdout.fileno(), b'\x07' )
				
			# Backspace
			elif key == "\x7f":
				if len(line) > 0 and lineIndex > 0:
					line = line[:lineIndex - 1] + line[lineIndex:]
					rewriteLine = True
					
				else:
					os.write( sys.stdout.fileno(), b'\x07' )
				
			# Printable character
			elif len(key) == 1 and ord(key) >= 32:
				line = line[:lineIndex] + key + line[lineIndex:]
				lineIndex += 1
				
				rewriteLine = True
		
			# Print the line to the console
			if rewriteLine:
				for i in range( 0, lastLineIndex ):
					os.write( sys.stdout.fileno(), b'\b' )
					
				os.write( sys.stdout.fileno(), line.encode( "ASCII" ) )
				
				for i in range( 0, len(line) - lineIndex ):
					os.write( sys.stdout.fileno(), b'\b' )
					
				lastLineIndex = lineIndex
		
		os.write( sys.stdout.fileno(), b'\n' )
		return line
		
		
	def print( self, message, end="\n", leftText="", lpad=0 ):
		lineLength = self._width - lpad
		linesPrinted = 0
		i = 0
		
		while i < len( message ):
			pad = leftText if i == 0 else ""
			line = message[i:i+lineLength]
			i += lineLength
			print( "%s%s" % ( pad.ljust( lpad ), line ), end=end )
			linesPrinted += 1
		
		return linesPrinted
	
	
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
				description = self._commands[command]["description"] if "description" in self._commands[command] else "No description available."
				lines = self.print( description, leftText=command, lpad=commandNameLength )
					
				# Look for command aliases
				aliases = []
				
				for alias in self._commands:
					if "alias" in self._commands[alias] and self._commands[alias]["alias"] == command:
						aliases.append( alias )
				
				# Print aliases' list if any
				if len(aliases):
					aliasTitle = "%sAliases: " % "".ljust( commandNameLength )
					lines += self.print( ", ".join( aliases ), leftText=aliasTitle, lpad=len( aliasTitle ) )
				
				# If the command's information is larger than 1 line, empty line is added
				if lines > 1:
					print( "" )
				
				
	def run( self, args=[] ):
		self._running = True
		separatorPattern = re.compile( '\s+' )
		
		while self._running:
			try:
				commandline = self.input( "%s > " % self._title )
				command = None
			
				# Parse arguments
				# TODO: Parse "" literals as one argument 
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
	
