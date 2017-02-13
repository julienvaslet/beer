# -*- coding: utf-8 -*-

import sys
import re
import os
import tty
import termios

from .command import *

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
		self._commands = {}
		
		self.addCommand( ExitCommand() )
		self.addCommand( HelpCommand() )
		
		
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
		
		
	def autocomplete( self, line ):
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

		args = []
		matches = re.findall( r'"([^"]*)"|([^\s]+)', line )
		
		for match in matches:
			args.append( match[0] if len( match[0] ) else match[1] )
		
		if keepTrailingSpace:
			if re.search( r"[^\s]+\s+$", line ) and keepTrailingSpace:
				args.append( "" )
		
		return args


	def input( self, prompt="" ):
		
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
	
