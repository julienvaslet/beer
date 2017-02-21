# -*- coding: utf-8 -*-
from .shell import *
from language import Language

class Command():
	"""Represents a shell command.
	
	Commands must inherit this class and provide an implemention of the
	run() method. The description and long description should be defined
	with the `Language` class and are autoloaded at command initialization.
	
	Attributes:
		- (str) _name: The name of the command.
		- (list) _aliases: The aliases' list of the command.
		- (str) _description: The short description of the command.
		- (str) _longDescription: The long description of the command.
	"""

	def __init__( self, name ):
		"""Initialize a command.
		
		Parameters:
			- (str) name: The name of the command.
		"""
		
		self._name = name
		self._aliases = []
		self._description = Language.get( self.__class__, "description" )
		self._longDescription = Language.get( self.__class__, "long_description" )


	def	getName( self ):
		"""Returns the name of the command."""
	
		return self._name
		
		
	def getDescription( self ):
		"""Returns the short description of the command, or an unavailable message."""
	
		return self._description if len(self._description) > 0 else "No description available."
		
		
	def getLongDescription( self ):
		"""Returns the long description of the command, or the short one if unavailable."""
		
		return self._longDescription if len(self._longDescription) > 0 else self.getDescription()
		
	
	def getAliases( self ):
		"""Returns the aliases' list of the command."""
		
		return self._aliases
		
		
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


class ExitCommand(Command):
	"""Represents the `exit` command to ends the shell sessions."""

	def __init__( self ):
		Command.__init__( self, "exit" )
		self._aliases = [ "quit" ]
	
	
	def run( self, shell, args ):
		shell.exit()
		
		return 0

		
class HelpCommand(Command):
	"""Represents the `help` command to show the shell available commands."""

	def __init__( self ):
		Command.__init__( self, "help" )
	
	def run( self, shell, args ):
	
		if len(args) > 1:
			if args[1] in shell._commands:
				commandName = args[1]
				
				# Avoid cyclic-dependencies
				testedNames = []
		
				while isinstance( shell._commands[commandName], str ) and commandName not in testedNames:
					testedNames.append( commandName )
					commandName = shell._commands[commandName]
					
				if isinstance( shell._commands[commandName], Command ):
					if args[1] == commandName:
						shell.print( Language.get( HelpCommand, "help_of_command" ) % commandName, lpad=1 )
					else:
						shell.print( Language.get( HelpCommand, "help_of_alias" ) % (args[1], commandName), lpad=1 )
					
					shell.print( "" )
					shell.print( shell._commands[commandName].getLongDescription(), lpad=2 )
					
				else:
					shell.error( Language.get( HelpCommand, "unknown_command" ) % args[1] )
				
			else:
				shell.error( Language.get( HelpCommand, "unknown_command" ) % args[1] )
		
		else:
			shell.print( "%s\n" % Language.get( HelpCommand, "commands_list" ), lpad=1 )
		
			commandNameLength = 0
		
			for command in shell._commands:
				if commandNameLength < len(command):
					commandNameLength = len(command)
	
			commandNameLength += 5
		
			for commandName in shell._commands:
				command = shell._commands[commandName]
			
				if isinstance( command, Command ):
					description = command.getDescription()
					lines = shell.print( description, leftText=" %s" % commandName, lpad=commandNameLength )
			
					# Print aliases' list if any
					if len(command.getAliases()):
						aliasTitle = "%s%s " % ( "".ljust( commandNameLength ), Language.get( HelpCommand, "aliases" ) )
						lines += shell.print( ", ".join( command.getAliases() ), leftText=aliasTitle, lpad=len( aliasTitle ) )
		
					# If the command's information is larger than 1 line, empty line is added
					if lines > 1:
						shell.print( " " )
		
		return 0


	def autocomplete( self, shell, args ):
	
		choices = []
		
		if len(args) == 2:
		
			for commandName in shell._commands:
				if commandName == "help":
					continue
			
				if commandName[:len(args[1])] == args[1]:
					choices.append( commandName )
		
		return choices
		
