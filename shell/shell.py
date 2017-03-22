# -*- coding: utf-8 -*-

import sys
import re
import os
import tty
import termios

from . import commands
from language import Language

WORD_SEPARATORS = [ " ", ",", ".", ";", ":", "!", "+", "-", "*", "/", "\\", "=", "(", ")", "{", "}", "[", "]", "^", "&", "|", ">", "<" ]

class Shell():
	"""Represents an interactive command interpreter.
	
	Verbosities are:
		- 0: quiet
		- 1: normal
		- 2: user debug
		- 3: shell debug
	
	Attributes:
		- (str) _title: Title of shell prompts.
		- (int) _width: Width of the shell (default: 79).
		- (bool) _running: Status of the shell session.
		- (int) _verbosity: Level of verbosity (default: 1).
		- (dict) _commands: Dictionary of registered commands.
	"""

	def __init__( self, title="", verbosity=1 ):
		"""Initialize a new shell."""

		# Load localized strings
		Language.load( "shell.ini" )
		
		self._title = title
		self._width = 79
		self._running = False
		self._verbosity = verbosity
		self._commands = {}
		
		self.add_command( commands.Exit() )
		self.add_command( commands.Help() )
		
		
	def error( self, message, code=0 ):
		"""Prints an error message to the standard error output.
		
		Prints an error message to the standard error output. If an error code
		greater than 0 is passed, it is prefixed to the message.
		
		Parameters:
			- (str) message: The error message to print.
			- (int) code: The error code associated to the message (default: 0)
		"""
		
		if code > 0:
			message = Language.get( Shell, "error_number" ) % ( code, message )
			
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
			self.print( message, left_text="[*]", lpad=4 )
			
	
	def warn( self, message, level=1 ):
		"""Prints a warning message to the shell output.
		
		Prints a warning message to the shell output. If the level is
		lower than the shell verbosity, the message is ignored.
		
		Parameters:
			- (str) message: The warning message to print.
			- (int) level: The level of verbosity of the message (default: 1).
		"""
		
		if level <= self._verbosity:
			self.print( message, left_text="[!]", lpad=4 )
			
			
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
		old_settings = termios.tcgetattr( fd )
		new_settings = termios.tcgetattr( fd )
		new_settings[3] = new_settings[3] & ~termios.ICANON & ~termios.ECHO
		new_settings[6][termios.VMIN] = 1
		new_settings[6][termios.VTIME] = 0

		termios.tcsetattr( fd, termios.TCSANOW, new_settings )
		
		escape_regex = re.compile( b'^(\xc2|\xc3|\x1b(O|\[([0-9]+(;([0-9]+)?)?)?)?)$' )

		try:
			complete = False
			
			while not complete:
				sequence += os.read( fd, 1 )
			
				if not escape_regex.match( sequence ):
					complete = True

		finally:
			termios.tcsetattr( fd, termios.TCSADRAIN, old_settings )

		return sequence
		
		
	def autocomplete( self, line ):
		"""Gets the autocompletion choices according to the current command line.
		
		Parameters:
			- (str) line: The current command line.
		
		Returns:
			- list -- the current available choices.
		"""
		
		choices = []
		
		args = self.parse_line( line, keep_trailing_space=True )
		
		if len(args) == 1:
			for command_name in self._commands:
				if command_name[:len(args[0])] == args[0]:
					choices.append( command_name )
					
		elif len(args) > 1:
			command = self.get_command( args[0] )
			
			if command != None:
				choices = command.autocomplete( self, args )
		
		return choices
		
		
	def parse_line( self, line, keep_trailing_space=False ):
		"""Parses the specified command line into an arguments array.
		
		Parses the specified command line into an arguments array. If the
		keep_trailing_space boolean is set and the command line ends with spaces,
		an empty string is added to the arguments list.
		
		Parameters:
			- (str) line: The command line.
			- (bool) keep_trailing_space: Keep trailing spaces (default: False).
		
		Returns:
			- list -- the arguments.
		"""

		args = []
		matches = re.findall( r'"([^"]*)"|([^\s]+)', line )
		
		for match in matches:
			args.append( match[0] if len( match[0] ) else match[1] )
		
		if keep_trailing_space:
			if re.search( r"[^\s]+\s+$", line ) and keep_trailing_space:
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
		line_index = 0
		last_line_index = 0
		last_length = 0
		line_read = False
		rewrite_line = False
		should_beep = False
		new_line = True
		
		while not line_read:
		
			# Print the line to the console
			if new_line:
				output = prompt + line + "\b" * (len(line) - line_index)
				os.write( sys.stdout.fileno(), output.encode() )
				
				new_line = False
			
			elif rewrite_line:
				output = ("\b" * last_line_index) + line
				
				if last_length > len(line):
					output += " " * (last_length - len(line))
					output += "\b" * (last_length - len(line))
					
				output += "\b" * (len(line) - line_index)
				
				os.write( sys.stdout.fileno(), output.encode() )
			
			# Emits console beep
			elif should_beep:
				os.write( sys.stdout.fileno(), b"\x07" )
			
			rewrite_line = False
			should_beep = False
			last_line_index = line_index
			last_length = len(line)
		
			rawkey = self.getch()
			
			try:
				#print( rawkey )
				key = rawkey.decode( "utf-8" )
				
			except UnicodeDecodeError:
				continue
			
			# End of line
			if key == "\x0a":
				line_read = True
				
			# Home
			elif key == "\x1b[H":
				line_index = 0
				rewrite_line = True
				
			# End
			elif key == "\x1b[F":
				line_index = len(line)
				rewrite_line = True
			
			# Tabulation
			elif key == "\x09":
				choices = self.autocomplete( line )
				
				if len(choices) > 0:
					# Prettify line
					args = self.parse_line( line, keep_trailing_space=True )
					line = " ".join( args )
					
					characters_to_be_replaced = 1
					
					while characters_to_be_replaced < len(line) and line[-characters_to_be_replaced:].lower() != choices[0][:characters_to_be_replaced].lower():
						characters_to_be_replaced += 1
						
					# There is no concordance
					if characters_to_be_replaced + 1 == len(line):
						characters_to_be_replaced = 0
					
					if len(choices) == 1:
						line = line[:(len(line)-characters_to_be_replaced)] + choices[0] + " "
						line_index = len(line)
						rewrite_line = True
						
					else:
						# Partial autocompletion
						similar_characters = 0

						while similar_characters < len(choices[0]):
							is_similar = True
							
							for choice in choices:
								if choice[similar_characters] != choices[0][similar_characters]:
									is_similar = False
									break
								
							if is_similar:
								similar_characters += 1
								
							else:
								break
						
						if similar_characters > 1 and similar_characters > characters_to_be_replaced:
							line = line[:(len(line)-characters_to_be_replaced)] + choices[0][:similar_characters]
							line_index = len(line)
							rewrite_line = True
							
						
						# Prints available choices
						max_choice_length = 0
						
						for choice in choices:
							if len(choice) > max_choice_length:
								max_choice_length = len(choice)
								
						max_choice_length += 2
						choice_line_length = 0
						
						output = "\n"
						
						for choice in choices:
							if choice_line_length + max_choice_length > self._width:
								choice_line_length = 0
								output += "\n"
								
							output += choice.ljust( max_choice_length )
							choice_line_length += max_choice_length
							
						output += "\n"
						
						os.write( sys.stdout.fileno(), output.encode() )
						new_line = True
				else:
					should_beep = True
				
			# Up
			#elif key == "\x1b[A":
			#	print( "UUUUP" )
				
			# Down
			#elif key == "\x1b[B":
			#	print( "DOOOWN" )
			
			# Left
			elif key == "\x1b[D":
			
				if line_index > 0:
					line_index -= 1
					rewrite_line = True
				
				else:
					should_beep = True
					
			# Ctrl+Left
			# Jump at the beginning of the word
			elif key == "\x1b[1;5D":
			
				# Purge separators
				while line_index > 0 and line[line_index - 1] in WORD_SEPARATORS:
					line_index -= 1
			
				# Jump at the beginning of current word
				while line_index > 0 and line[line_index - 1] not in WORD_SEPARATORS:
					line_index -= 1
					
				rewrite_line = True
			
			# Right
			elif key == "\x1b[C":
			
				if line_index < len(line):
					line_index += 1
					rewrite_line = True
				
				else:
					should_beep = True
			
			# Ctrl+Right
			# Jump at the end of the word
			elif key == "\x1b[1;5C":
			
				# Purge separators
				while line_index < len(line) and line[line_index] in WORD_SEPARATORS:
					line_index += 1
			
				# Jump at the next separator
				while line_index < len(line) and line[line_index] not in WORD_SEPARATORS:
					line_index += 1
					
				rewrite_line = True
				
			# Backspace
			elif key == "\x7f":
				if len(line) > 0 and line_index > 0:
					line = line[:line_index - 1] + line[line_index:]
					line_index -= 1
					rewrite_line = True
					
				else:
					should_beep = True
					
			# Delete
			elif key == "\x1b[3~":
				if len(line) > 0 and line_index < len(line):
					line = line[:line_index] + line[line_index + 1:]
					rewrite_line = True
					
				else:
					should_beep = True
				
			# Printable character
			elif len(key) == 1 and ord(key) >= 32:
				line = line[:line_index] + key + line[line_index:]
				line_index += 1
				
				rewrite_line = True
		
		os.write( sys.stdout.fileno(), b"\n" )
		return line
		
		
	def print( self, message, end="\n", left_text="", lpad=0, break_words=False, justify_text=True ):
		"""Prints a message to the shell output.
		
		Prints a message to the shell output. This message could be left-padded
		in order to indent it and a message can be added into the left-padding.
		
		Parameters:
			- (str) message: The message to print.
			- (str) end: The end of message separator (default "\n").
			- (str) left_text: The text printed in the left padding (default: "").
			- (int) lpad: The left padding width (default: 0).
			- (bool) break_words: Break too long words at end of lines (default: False).
			- (bool) justify_text: Change the words spacing to fit the shell width (default: True).
		
		Returns:
			- int -- the number of lines printed.
		"""
		
		line_length = self._width - lpad
		lines_printed = 0
		
		for msg in re.split( r"\n", message ):
			
			if len( msg ) == 0:
				print( "", end=end )
				lines_printed += 1
				
			else:
				i = 0
				while i < len( msg ):
					pad = left_text if i == 0 else ""
					
					current_line_length = line_length if i + line_length < len(msg) else len(msg) - i
					
					if not break_words and i + current_line_length < len(msg):
						while current_line_length > 0 and msg[i+current_line_length] != " ":
							current_line_length -= 1
					
						# Line does not contains any spaces, words are breaked.
						if current_line_length == 0:
							current_line_length = line_length
					
					line = msg[i:i+current_line_length].strip()
					i += current_line_length
					
					# Justify active, smaller line than shell with, and not the last one.
					if justify_text and len(line) < line_length and i < len(msg):
						spaces_to_add = line_length - len(line)
						spaces = len(re.findall( r"\s+", line ))
						extended_spaces = len(re.findall( r"[,\.]\s", line ))
						
						if spaces > 0 and spaces_to_add >= 2 * spaces:
							space_width = spaces_to_add // spaces
							spaces_to_add -= space_width
							line = line.replace( " ", " " * space_width )
							
						if extended_spaces > 0:
							extended_space_width = spaces_to_add // extended_spaces
							spaces_to_add = spaces_to_add % extended_spaces
							
							line = re.sub( r"([,\.]\s)", r"\1%s" % ( " " * extended_space_width ), line )
							
							# Remaining spaces
							if spaces_to_add > 0:
								line = re.sub( r"([,\.]\s)", r"\1 ", line, count=spaces_to_add )
								spaces_to_add = 0
						
						# Remaining spaces (for lines without punctuation)
						if spaces_to_add > 0:
							line = re.sub( r"(\s)", r"\1 ", line, count=spaces_to_add )
							spaces_to_add = 0
						
					print( "%s%s" % ( pad.ljust( lpad ), line ), end=end )
					lines_printed += 1
		
		return lines_printed
		
	
	def add_command( self, command ):
		"""Adds a command to the shell.
		
		Parameters:
			- (shell.commands.Command) command: The command to add.
		"""
	
		if isinstance( command, commands.Command ):
			
			if command.name in self._commands:
				self.log( Language.get( Shell, "replacing_command" ) % command.name, level=3 )
			else:
				self.log( Language.get( Shell, "loading_command" ) % command.name, level=3 )
			
			self._commands[command.name] = command
			
			for alias in command.aliases:
				if alias not in self._commands:
					self.log( Language.get( Shell, "adding_alias" ) % ( alias, command.name ), level=3 )
					self._commands[alias] = command.name
					
				else:
					self.log( Language.get( Shell, "ignoring_alias" ) % alias, level=3 )
			
		else:
			self.error( Language.get( Shell, "command_not_loaded" ) )
	
	
	def get_command( self, command_name ):
		command = None
	
		if command_name in self._commands:
			# Avoid cyclic-dependencies
			tested_names = []
	
			while isinstance( self._commands[command_name], str ) and command_name not in tested_names:
				tested_names.append( command_name )
				command_name = self._commands[command_name]
	
			if isinstance( self._commands[command_name], commands.Command ):
				command = self._commands[command_name]
				
		return command
	
	
	def execute( self, args=[] ):
		"""Executes a parsed command line.
		
		Parameters:
			- (list) args: The parsed command line.
		"""
		
		command = self.get_command( args[0] )
		
		if command != None:
			command.run( self, args )
		else:
			self.error( Language.get( Shell, "unknown_command" ) % args[0] )
	
				
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
					args = self.parse_line( commandline )

					if len( args ) == 0:
						continue
			
					self.execute( args )
			
				except KeyboardInterrupt:
					print()
					self.log( Language.get( Shell, "interrupt_by_user" ), level=0 )
					self.exit()
		
		# Single command execution		
		else:
			self.execute( args )
	
