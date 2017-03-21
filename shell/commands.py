# -*- coding: utf-8 -*-
from .shell import *
from language import Language

class Command():
	"""Represents a shell command.
	
	Commands must inherit this class and provide an implemention of the
	run() method. The description and long description should be defined
	with the `Language` class and are autoloaded at command initialization.
	
	Attributes:
		- (str) name: The name of the command.
		- (list) aliases: The aliases' list of the command.
		- (str) _description: The short description of the command.
		- (str) _long_description: The long description of the command.
	"""
	
	_options = {}
	

	def __init__( self, name ):
		"""Initialize a command.
		
		Parameters:
			- (str) name: The name of the command.
		"""
		
		self.name = name
		self.aliases = []
		self._description = Language.get( self.__class__, "description" )
		self._long_description = Language.get( self.__class__, "long_description" )

		
	@property
	def description( self ):
		"""Returns the short description of the command, or an unavailable message."""
	
		return self._description if len(self._description) > 0 else "No description available."
		
	
	@property
	def long_description( self ):
		"""Returns the long description of the command, or the short one if unavailable."""
		
		return self._long_description if len(self._long_description) > 0 else self.description
		
		
	def run( self, shell, args ):
		"""Runs the command.
		
		Parameters:
			- (shell.shell.Shell) shell: The invoker shell.
			- (list) args: The command line arguments.
		"""
		
		raise NotImplementedError()
		
	
	def autocomplete( self, shell, args ):
		"""Query the command autocompletion.
		
		Parameters:
			- (shell.shell.Shell) shell: The invoker shell.
			- (list) args: The command line arguments.
		"""
		
		return []
		
		
	@classmethod
	def parse_options( cls, args ):
		
		print( cls._options )
	
		return {}


class Exit(Command):
	"""Represents the `exit` command to ends the shell sessions."""

	def __init__( self ):
		Command.__init__( self, "exit" )
		self.aliases = [ "quit" ]
	
	
	def run( self, shell, args ):
		shell.exit()
		
		return 0

		
class Help(Command):
	"""Represents the `help` command to show the shell available commands."""

	def __init__( self ):
		Command.__init__( self, "help" )
	
	def run( self, shell, args ):
	
		if len(args) > 1:
			if args[1] in shell._commands:
				command_name = args[1]
				
				# Avoid cyclic-dependencies
				tested_names = []
		
				while isinstance( shell._commands[command_name], str ) and command_name not in tested_names:
					tested_names.append( command_name )
					command_name = shell._commands[command_name]
					
				if isinstance( shell._commands[command_name], Command ):
					if args[1] == command_name:
						shell.print( Language.get( Help, "help_of_command" ) % command_name, lpad=1 )
					else:
						shell.print( Language.get( Help, "help_of_alias" ) % (args[1], command_name), lpad=1 )
					
					shell.print( "" )
					shell.print( shell._commands[command_name].long_description, lpad=2 )
					
				else:
					shell.error( Language.get( Help, "unknown_command" ) % args[1] )
				
			else:
				shell.error( Language.get( Help, "unknown_command" ) % args[1] )
		
		else:
			shell.print( "%s\n" % Language.get( Help, "commands_list" ), lpad=1 )
		
			command_name_length = 0
		
			for command in shell._commands:
				if command_name_length < len(command):
					command_name_length = len(command)
	
			command_name_length += 5
		
			for command_name in shell._commands:
				command = shell._commands[command_name]
			
				if isinstance( command, Command ):
					lines = shell.print( command.description, left_text=" %s" % command_name, lpad=command_name_length )
			
					# Print aliases' list if any
					if len(command.aliases):
						alias_title = "%s%s " % ( "".ljust( command_name_length ), Language.get( Help, "aliases" ) )
						lines += shell.print( ", ".join( command.aliases ), left_text=alias_title, lpad=len( alias_title ) )
		
					# If the command's information is larger than 1 line, empty line is added
					if lines > 1:
						shell.print( "" )
		
		return 0


	def autocomplete( self, shell, args ):
	
		choices = []
		
		if len(args) == 2:
		
			for command_name in shell._commands:
				if command_name == "help":
					continue
			
				if command_name[:len(args[1])] == args[1]:
					choices.append( command_name )
		
		return choices
		
