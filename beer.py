#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import log
from language import Language
from beershell import *
from brewery.ingredients import *
from units import *

if __name__ == "__main__":

	argv = list(sys.argv)
	argv.pop( 0 )
	
	if len(argv) > 0 and argv[0] == "autocomplete":
		argv.pop( 0 )
	
		if len(argv) > 0:
			Language.initialize( lang="en" )
			Language.load( "hops.ini" )
			Language.load( "ingredients.ini" )
			ingredient.Ingredient.load_directory( "data%singredients" % os.sep )
	
			shell = beershell.BeerShell( verbosity=0 )
			choices = shell.autocomplete( argv[0] )
		
		if len(choices):
			print( "\n".join( choices ) )
	
	else:
		# Development needs
		log.verbosity = 3
	
		Language.initialize( lang="en" )
		Language.load( "hops.ini" )
		Language.load( "yeasts.ini" )
		Language.load( "ingredients.ini" )
		ingredient.Ingredient.load_directory( "data%singredients" % os.sep )
	
		shell = beershell.BeerShell( verbosity=log.verbosity )
		log.current_shell = shell
	
		shell.run( argv )
