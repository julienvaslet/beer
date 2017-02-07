# -*- coding: utf-8 -*-

import sys
import re
import os
import tty
import termios

escapeSequences = [
	b"\x1b",
	b"\x1b[",
	b"\x1b[1",		# Home, End
	b"\x1b[1;",
	b"\x1b[1;2",	# Ctrl+[Up,Down]
	b"\x1b[1;3",	# Alt+[Up,Down,Left,Right]
	b"\x1b[1;4",	# Maj+Alt+[F2,F3,F4]
	b"\x1b[1;5",	# Ctrl+[Left,Right]
	b"\x1b[1;6",	# Ctrl+Maj+[Left,Right]
	b"\x1b[15",		# F5
	b"\x1b[15;",
	b"\x1b[15;2",	# Maj+F5
	b"\x1b[15;4",	# Alt+Maj+F5
	b"\x1b[15;5",	# Ctrl+F5
	b"\x1b[17",		# F6
	b"\x1b[17;",
	b"\x1b[17;2",	# Maj+F6
	b"\x1b[17;5",	# Ctrl+F6
	b"\x1b[18",		# F7
	b"\x1b[18;",
	b"\x1b[18;2",	# Maj+F7
	b"\x1b[18;4",	# Alt+Maj+F7
	b"\x1b[18;5",	# Ctrl+F7
	b"\x1b[19",		# F8
	b"\x1b[19;",
	b"\x1b[19;2",	# Maj+F8
	b"\x1b[19;4",	# Alt+Maj+F8
	b"\x1b[19;5",	# Ctrl+F8
	b"\x1b[2",		# Insert
	b"\x1b[2;",
	b"\x1b[2;3",	# Maj+Insert
	b"\x1b[2;6",	# Ctrl+Maj+Insert
	b"\x1b[20",		# F9
	b"\x1b[20;",
	b"\x1b[20;2",	# Maj+F9
	b"\x1b[20;4",	# Alt+Maj+F9
	b"\x1b[20;5",	# Ctrl+F9
	b"\x1b[24",		# F12
	b"\x1b[24;",
	b"\x1b[24;2",	# Maj+F12
	b"\x1b[24;4",	# Alt+Maj+F12
	b"\x1b[24;5",	# Ctrl+F12
	b"\x1b[3",		# Delete
	b"\x1b[3;",
	b"\x1b[3;2",	# Maj+Delete
	b"\x1b[3;3",	# Alt+Delete
	b"\x1b[3;4",	# Alt+Maj+Delete
	b"\x1b[3;5",	# Ctrl+Delete
	b"\x1b[3;6",	# Ctrl+Maj+Delete
	b"\x1b[5",		# Page-Up
	b"\x1b[5;",
	b"\x1b[5;3",	# Alt+Page-Up
	b"\x1b[6",		# Page-Down
	b"\x1b[6;",
	b"\x1b[6;3",	# Alt+Page-Down
	b"\x1bO",		# F2, F3, F4
	b"\xc3"			# Unicode
]

wordSeparators = [ " ", ",", ".", ";", ":", "!", "+", "-", "*", "/", "\\", "=", "(", ")", "{", "}", "[", "]", "^", "&", "|", ">", "<" ]

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
		sequence = b""

		fd = sys.stdin.fileno()
		oldSettings = termios.tcgetattr( fd )
		newSettings = termios.tcgetattr( fd )
		newSettings[3] = newSettings[3] & ~termios.ICANON & ~termios.ECHO
		newSettings[6][termios.VMIN] = 1
		newSettings[6][termios.VTIME] = 0

		termios.tcsetattr( fd, termios.TCSANOW, newSettings )

		try:
			complete = False
			
			while not complete:
				sequence += os.read( fd, 1 )
			
				if sequence not in escapeSequences:
					complete = True

		finally:
			termios.tcsetattr( fd, termios.TCSADRAIN, oldSettings )

		return sequence


	def input( self, prompt="" ):
		
		if len( prompt ):
			os.write( sys.stdout.fileno(), prompt.encode( "ASCII" ) )
		
		line = ""
		lineIndex = 0
		lastLineIndex = 0
		lastLength = 0
		lineRead = False
		
		while not lineRead:
			rawkey = self.getch()
			rewriteLine = False
			shouldBeep = False
			
			try:
				key = rawkey.decode( "utf-8" )
				#print( rawkey )
				
			except UnicodeDecodeError:
				continue
			
			# End of line
			if key == "\x0a":
				lineRead = True
				
			# Home
			elif key == "\x1b[H":
				lineIndex = 0
				rewriteLine = True
				
			# End
			elif key == "\x1b[F":
				lineIndex = len(line)
				rewriteLine = True
			
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
					shouldBeep = True
					
			# Ctrl+Left
			# Jump at the beginning of the word
			elif key == "\x1b[1;5D":
			
				# Purge separators
				while lineIndex > 0 and line[lineIndex - 1] in wordSeparators:
					lineIndex -= 1
			
				# Jump at the beginning of current word
				while lineIndex > 0 and line[lineIndex - 1] not in wordSeparators:
					lineIndex -= 1
					
				rewriteLine = True
			
			# Right
			elif key == "\x1b[C":
			
				if lineIndex < len(line):
					lineIndex += 1
					rewriteLine = True
				
				else:
					shouldBeep = True
			
			# Ctrl+Right
			# Jump at the end of the word
			elif key == "\x1b[1;5C":
			
				# Purge separators
				while lineIndex < len(line) and line[lineIndex] in wordSeparators:
					lineIndex += 1
			
				# Jump at the next separator
				while lineIndex < len(line) and line[lineIndex] not in wordSeparators:
					lineIndex += 1
					
				rewriteLine = True
				
			# Backspace
			elif key == "\x7f":
				if len(line) > 0 and lineIndex > 0:
					line = line[:lineIndex - 1] + line[lineIndex:]
					lineIndex -= 1
					rewriteLine = True
					
				else:
					shouldBeep = True
				
			# Printable character
			elif len(key) == 1 and ord(key) >= 32:
				line = line[:lineIndex] + key + line[lineIndex:]
				lineIndex += 1
				
				rewriteLine = True
		
		
			# Print the line to the console
			if rewriteLine:
				for i in range( 0, lastLineIndex ):
					os.write( sys.stdout.fileno(), b"\b" )
					
				os.write( sys.stdout.fileno(), line.encode() )
				
				if lastLength > len(line):
					for i in range( 0,lastLength - len(line) ):
						os.write( sys.stdout.fileno(), b" " )
						
					for i in range( 0,lastLength - len(line) ):
						os.write( sys.stdout.fileno(), b"\b" )
				
				for i in range( 0, len(line) - lineIndex ):
					os.write( sys.stdout.fileno(), b"\b" )
			
			# Emits console beep
			elif shouldBeep:
				os.write( sys.stdout.fileno(), b"\x07" )
			
			
			lastLineIndex = lineIndex
			lastLength = len(line)
				
		
		os.write( sys.stdout.fileno(), b"\n" )
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
		separatorPattern = re.compile( "\s+" )
		
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
	
