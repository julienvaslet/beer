# -*- coding: utf-8 -*-

from shell import *

class BeerShell(shell.Shell):

	def __init__( self ):
		shell.Shell.__init__( self, title="beer" )
	
	
	def banner( self ):
		self.print( " " )
		self.print( "╻ ╻   ┏┓ ┏━╸┏━╸┏━┓   ╻" )
		self.print( "╺╋╸   ┣┻┓┣╸ ┣╸ ┣┳┛   ╹" )
		self.print( "╹ ╹   ┗━┛┗━╸┗━╸╹┗╸   ╹" )
		self.print( "╺━━━━━━━━━━━━━━━━━━━━╸" )
	
	
	def run( self, args=[] ):
		self.banner()
		self.print( " " )
		self.log( "Recipes: %d" % 0 )
		self.log( "Malts: %d" % 0 )
		self.log( "Hops: %d" % 0 )
		self.print( " " )
	
		shell.Shell.run( self, args )
