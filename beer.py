#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from beershell import *

if __name__ == "__main__":

	argv = sys.argv
	argv.pop( 0 )
	
	shell = beershell.BeerShell()
	shell.run( argv )
