#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import log
from language import Language
from beershell import *

if __name__ == "__main__":

	# Development needs
	log.verbosity = 3
	
	Language.initialize( lang="en" )

	argv = sys.argv
	argv.pop( 0 )
	
	shell = beershell.BeerShell( verbosity=log.verbosity )
	log.currentShell = shell
	
	shell.run( argv )
