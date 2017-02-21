# -*- coding: utf-8 -*-

from shell import *
from language import Language
from . import convertcommand

class BeerShell(shell.Shell):

	def __init__( self ):
		shell.Shell.__init__( self, title="beer" )
		Language.load( "beershell.ini" )
		self.addCommand( convertcommand.ConvertCommand() )
	
	def banner( self ):
		self.print( "" )
		self.print( "╻ ╻   ┏┓ ┏━╸┏━╸┏━┓   ╻" )
		self.print( "╺╋╸   ┣┻┓┣╸ ┣╸ ┣┳┛   ╹" )
		self.print( "╹ ╹   ┗━┛┗━╸┗━╸╹┗╸   ╹" )
		self.print( "╺━━━━━━━━━━━━━━━━━━━━╸" )
	
	
	def run( self, args=[] ):
	
		if len( args ) == 0:
			self.banner()
			self.print( "" )
			self.log( "Recipes: %d" % 0 )
			self.log( "Malts: %d" % 0 )
			self.log( "Hops: %d" % 0 )
			
			#self.log( "Planned: %d" % 0 )
			#self.log( "In fermentation: %d" % 0 )
			self.print( "" )
	
		shell.Shell.run( self, args )
