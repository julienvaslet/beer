#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import log

# Setting correct working directory
os.chdir( os.path.dirname( os.path.realpath( os.path.abspath( sys.argv[0] ) ) ) )

from language import Language
from beershell import *
from brewery.ingredients import *
from units import *

if __name__ == "__main__":

	# Development needs
	log.verbosity = 3
	
	Language.initialize( lang="en" )
	Language.load( "hops.ini" )
	Language.load( "ingredients.ini" )
	ingredient.Ingredient.load_directory( "data%singredients" % os.sep )

	argv = sys.argv
	argv.pop( 0 )
	
	shell = beershell.BeerShell( verbosity=log.verbosity )
	log.current_shell = shell
	
	shell.run( argv )
