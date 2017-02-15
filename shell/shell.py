# -*- coding: utf-8 -*-

import sys
import re
import os
import tty
import termios

from .command import *

wordSeparators = [ " ", ",", ".", ";", ":", "!", "+", "-", "*", "/", "\\", "=", "(", ")", "{", "}", "[", "]", "^", "&", "|", ">", "<" ]

class Shell():
	"""Represents an interactive command interpreter.
	
	Verbosities are:
		- 0: quiet
		- 1: normal
		- 2: user debug
		- 3: shell debug
	
	Attributes:
		- (str) _title: Title of shell prompts.
		- (int) _width: Width of the shell (default: 80).
		- (bool) _running: Status of the shell session.
		- (int) _verbosity: Level of verbosity (default: 1).
		- (dict) _commands: Dictionary of registered commands.
	"""

	def __init__( self, title="" ):
		"""Initialize a new shell."""
		
		self._title = title
		self._width = 80
		self._running = False
		self._verbosity = 1
		self._commands = {}
		
		self.addCommand( ExitCommand() )
		self.addCommand( HelpCommand() )
		
		
	def error( self, message, code=0 ):
		"""Prints an error message to the standard error output.
		
		Prints an error message to the standard error output. If an error code
		greater than 0 is passed, it is prefixed to the message.
		
		Parameters:
			- (str) message: The error message to print.
			- (int) code: The error code associated to the message (default: 0)
		"""
		
		if code > 0:
			message = "Error %d: %s" % ( code, message )
			
		print( "[!] %s" % message, file=sys.stderr )
		
		
	def log( self, message, level=1 ):
		"""Prints an informative message to the shell output.
		
		Prints an informative message to the shell output. If the level is
		lower than the shell verbosity, the message is ignored.
		
		Parameters:
			- (str) message: The message to print.
			- (int) level: The level of verbosity of the message (default: 1).
		"""
		
		if level <= self._verbosity:
			self.print( message, leftText="[*]", lpad=4 )
			
			
	def exit( self ):
		"""Ends the shell session."""
		
		self._running = False
	
	
	def getch( self ):
		"""Reads a character from user standard input.
		
		Reads a character or a sequence from the user standard input without
		printing it. Sequences are read to correctly get HOME, END, TAB, etc.
		keys and unicode characters.
		
		Returns:
			- bytes -- the raw bytes sequence read.
		"""
		
		sequence = b""

		fd = sys.stdin.fileno()
		oldSettings = termios.tcgetattr( fd )
		newSettings = termios.tcgetattr( fd )
		newSettings[3] = newSettings[3] & ~termios.ICANON & ~termios.ECHO
		newSettings[6][termios.VMIN] = 1
		newSettings[6][termios.VTIME] = 0

		termios.tcsetattr( fd, termios.TCSANOW, newSettings )
		
		escapeRegex = re.compile( b'^(\xc2|\xc3|\x1b(O|\[([0-9]+(;([0-9]+)?)?)?)?)$' )

		try:
			complete = False
			
			while not complete:
				sequence += os.read( fd, 1 )
			
				if not escapeRegex.match( sequence ):
					complete = True

		finally:
			termios.tcsetattr( fd, termios.TCSADRAIN, oldSettings )

		return sequence
		
		
	def autocomplete( self, line ):
		"""Gets the autocompletion choices according to the current command line.
		
		Parameters:
			- (str) line: The current command line.
		
		Returns:
			- list -- the current available choices.
		"""
		
		choices = []
		
		args = self.parseLine( line, keepTrailingSpace=True )
		
		if len(args) == 1:
			for commandName in self._commands:
				if commandName[:len(args[0])] == args[0]:
					choices.append( commandName )
					
		elif len(args) > 1:
			if args[0] in self._commands:
				choices = self._commands[args[0]].autocomplete( self, args )
		
		return choices
		
		
	def parseLine( self, line, keepTrailingSpace=False ):
		"""Parses the specified command line into an arguments array.
		
		Parses the specified command line into an arguments array. If the
		keepTrailingSpace boolean is set and the command line ends with spaces,
		an empty string is added to the arguments list.
		
		Parameters:
			- (str) line: The command line.
			- (bool) keepTrailingSpace: Keep trailing spaces (default: False).
		
		Returns:
			- list -- the arguments.
		"""

		args = []
		matches = re.findall( r'"([^"]*)"|([^\s]+)', line )
		
		for match in matches:
			args.append( match[0] if len( match[0] ) else match[1] )
		
		if keepTrailingSpace:
			if re.search( r"[^\s]+\s+$", line ) and keepTrailingSpace:
				args.append( "" )
		
		return args


	def input( self, prompt="" ):
		"""Reads a command line from the user input.
		
		Reads a command line from the user input. Arrow keys, Home, End and Tab
		keys are intercepted to provide input navigation and autocompletion.
		
		Parameters:
			- (str) prompt: The prompt message.
			
		Returns:
			- str -- the read command line.
		"""
		
		line = ""
		lineIndex = 0
		lastLineIndex = 0
		lastLength = 0
		lineRead = False
		rewriteLine = False
		shouldBeep = False
		newLine = True
		
		while not lineRead:
		
			# Print the line to the console
			if newLine:
				output = prompt + line + "\b" * (len(line) - lineIndex)
				os.write( sys.stdout.fileno(), output.encode() )
				
				newLine = False
			
			elif rewriteLine:
				output = ("\b" * lastLineIndex) + line
				
				if lastLength > len(line):
					output += " " * (lastLength - len(line))
					output += "\b" * (lastLength - len(line))
					
				output += "\b" * (len(line) - lineIndex)
				
				os.write( sys.stdout.fileno(), output.encode() )
			
			# Emits console beep
			elif shouldBeep:
				os.write( sys.stdout.fileno(), b"\x07" )
			
			rewriteLine = False
			shouldBeep = False
			lastLineIndex = lineIndex
			lastLength = len(line)
		
			rawkey = self.getch()
			
			try:
				#print( rawkey )
				key = rawkey.decode( "utf-8" )
				
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
			elif key == "\x09":
				choices = self.autocomplete( line )
				
				if len(choices) > 0:
					if len(choices) == 1:
						args = self.parseLine( line, keepTrailingSpace=True )
						args[len(args) - 1] = choices[0] + " "
						
						line = " ".join( args )
						lineIndex = len(line)
						rewriteLine = True
						
					else:
						# Prints available choices
						maxChoiceLength = 0
						
						for choice in choices:
							if len(choice) > maxChoiceLength:
								maxChoiceLength = len(choice)
								
						maxChoiceLength += 2
						choiceLineLength = 0
						
						output = "\n"
						
						for choice in choices:
							if choiceLineLength + maxChoiceLength > self._width:
								choiceLineLength = 0
								output += "\n"
								
							output += choice.ljust( maxChoiceLength )
							
						output += "\n"
						
						os.write( sys.stdout.fileno(), output.encode() )
						newLine = True
				else:
					shouldBeep = True
				
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
					
			# Delete
			elif key == "\x1b[3~":
				if len(line) > 0 and lineIndex < len(line):
					line = line[:lineIndex] + line[lineIndex + 1:]
					rewriteLine = True
					
				else:
					shouldBeep = True
				
			# Printable character
			elif len(key) == 1 and ord(key) >= 32:
				line = line[:lineIndex] + key + line[lineIndex:]
				lineIndex += 1
				
				rewriteLine = True
		
		os.write( sys.stdout.fileno(), b"\n" )
		return line
		
		
	def print( self, message, end="\n", leftText="", lpad=0 ):
		"""Prints a message to the shell output.
		
		Prints a message to the shell output. This message could be left-padded
		in order to indent it and a message can be added into the left-padding.
		
		Parameters:
			- (str) message: The message to print.
			- (str) end: The end of message separator (default "\n").
			- (str) leftText: The text printed in the left padding (default: "").
			- (int) lpad: The left padding width (default: 0).
		
		Returns:
			- int -- the number of lines printed.
		"""
		
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
		
	
	def addCommand( self, command ):
		"""Adds a command to the shell.
		
		Parameters:
			- (shell.command.Command) command: The command to add.
		"""
	
		if isinstance( command, Command ):
			
			if command.getName() in self._commands:
				self.log( "Replacing existing command \"%s\"." % command.getName(), level=3 )
			else:
				self.log( "Loading command \"%s\"." % command.getName(), level=3 )
			
			self._commands[command.getName()] = command
			
			for alias in command.getAliases():
				if alias not in self._commands:
					self.log( "Adding alias \"%s\" for command \"%s\"." % ( alias, command.getName() ), level=3 )
					self._commands[alias] = command.getName()
					
				else:
					self.log( "Ignoring alias \"%s\" because a command exists with this name." % alias, level=3 )
			
		else:
			self.error( "Can not load command because it is not a \"shell.command.Command\" instance." )
	
	
	def execute( self, args=[] ):
		"""Executes a parsed command line.
		
		Parameters:
			- (list) args: The parsed command line.
		"""
		
		command = None
	
		if args[0] in self._commands:
			commandName = args[0]
		
			# Avoid cyclic-dependencies
			testedNames = []
		
			while isinstance( self._commands[commandName], str ) and commandName not in testedNames:
				testedNames.append( commandName )
				commandName = self._commands[commandName]
		
			if isinstance( self._commands[commandName], Command ):
				command = self._commands[commandName]
		
		if command != None:
			command.run( self, args )
		else:
			self.error( "Unknown command %s." % args[0] )
	
				
	def run( self, args=[] ):
		"""Launches the shell session.
		
		Parameters:
			- (list) args: Arguments passed to the shell.
		"""
	
		# Shell mode
		if len(args) == 0:
			self._running = True
		
			while self._running:
				try:
					commandline = self.input( "%s > " % self._title )
					args = self.parseLine( commandline )

					if len( args ) == 0:
						continue
			
					self.execute( args )
			
				except KeyboardInterrupt:
					print()
					self.log( "Interrupted by user.", level=0 )
					self.exit()
		
		# Single command execution		
		else:
			self.execute( args )
	
