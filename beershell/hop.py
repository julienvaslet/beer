# -*- coding: utf-8 -*-
from shell import *
from brewery.ingredients.hop import Hop
from language import Language

import re

class Command(commands.Command):

	def __init__( self ):
		commands.Command.__init__( self, "hop" )
		self._shell = Shell()
		
		
	def run( self, shell, args ):
	
		self._shell._verbosity = shell._verbosity
		
		args.pop( 0 )
		self._shell.run( args )
		
		return 0
		
		
	def autocomplete( self, shell, args ):
	
		choices = []	
		return choices


class Shell(shell.Shell):
	
	def __init__( self, verbosity=1 ):
		shell.Shell.__init__( self, title="hop", verbosity=verbosity )
		self.add_command( List() )
		

class List(commands.Command):

	def __init__( self ):
		commands.Command.__init__( self, "list" )
		
		
	def run( self, shell, args ):
	
		hops = Hop.list_hops()
		
		for hop in hops:
			shell.print( "%s (%saa)" % ( hop.name, hop.alpha_acids ), lpad=1 )
			
		return 0
		
		
	def autocomplete( self, shell, args ):
	
		choices = []	
		return choices


