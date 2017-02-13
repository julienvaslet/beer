# -*- coding: utf-8 -*-
from .shell import *

class Command():

	def __init__( self, name, description="" ):
		self._name = name
		self._aliases = []
		self._description = description
		self._longDescription = ""


	def	getName( self ):
		return self._name
		
		
	def getDescription( self ):
		return self._description if len(self._description) > 0 else "No description available."
		
		
	def getLongDescription( self ):
		return self._longDescription if len(self._longDescription) > 0 else self.getDescription()
		
	
	def getAliases( self ):
		return self._aliases
		
		
	def run( self, shell, args ):
		raise NotImplementedError()
		
	
	def autocomplete( self, shell, args ):
		return []


class ExitCommand(Command):

	def __init__( self ):
		Command.__init__( self, "exit", description="Exits the current shell." )
		self._aliases = [ "quit" ]
	
	
	def run( self, shell, args ):
		shell.exit()
		
		return 0

		
class HelpCommand(Command):

	def __init__( self ):
		Command.__init__( self, "help", description="Show this help message." )
	
	def run( self, shell, args ):
	
		shell.print( "List of available commands:\n", lpad=1 )
		
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
					aliasTitle = "%sAliases: " % "".ljust( commandNameLength )
					lines += shell.print( ", ".join( command.getAliases() ), leftText=aliasTitle, lpad=len( aliasTitle ) )
		
				# If the command's information is larger than 1 line, empty line is added
				if lines > 1:
					shell.print( " " )
		
		return 0
