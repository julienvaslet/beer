#!/usr/bin/python3
# -*- coding: utf-8 -*-

from util import *
from units import *
from shell import Shell

if __name__ == "__main__":
	# Banner and summary
	banner()
	shell = Shell( "beer" )
	
	shell.print( "Recipes: %d" % 0, lpad=3 )
	shell.print( "Malts: %d" % 0, lpad=3 )
	shell.print( "Hops: %d\n" % 0, lpad=3 )
	
	shell.run()
	#a = unit.Unit()
