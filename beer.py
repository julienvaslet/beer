#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from language import Language
from beershell import *

if __name__ == "__main__":

	Language.initialize( lang="en" )

	argv = sys.argv
	argv.pop( 0 )
	
	shell = beershell.BeerShell()
	shell.run( argv )
