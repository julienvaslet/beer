#!/usr/bin/python3
# -*- coding: utf-8 -*-

from util import *
from units import *
from shell import *

if __name__ == "__main__":
	# Banner and summary
	banner()
	shell = shell.Shell( "beer" )
	
	shell.print( " " )
	shell.log( "Recipes: %d" % 0 )
	shell.log( "Malts: %d" % 0 )
	shell.log( "Hops: %d" % 0 )
	shell.print( " " )
	
	shell.run()
	#a = unit.Unit()
