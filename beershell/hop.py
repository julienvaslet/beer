# -*- coding: utf-8 -*-
from shell import *
from brewery.ingredients import *
from language import Language

import re

class Command(commands.Command):

	def __init__( self ):
		commands.Command.__init__( self, "hop" )
		
	
	# hop list purpose=[aroma|dual|bitterness] country=[a-z] ...
	# hop info <name> <attributes>
	def run( self, shell, args ):
	
		if len(args) < 2:
			shell.print( Language.get( Command, "help_message" ) % args[0], lpad=1 )
			return 1
		
		args.pop( 0 )
		s_value = args[0]
		args.pop( 0 )
		
		return 0
		
		
	def autocomplete( self, shell, args ):
	
		choices = []	
		return choices

