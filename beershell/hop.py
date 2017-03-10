# -*- coding: utf-8 -*-
from shell import *
from brewery.ingredients.hop import Hop
from language import Language

import re

class Command(commands.Command):

	def __init__( self ):
		commands.Command.__init__( self, "hop" )
		self._shell = Shell()
		
		
	def run( self, shell, args ):
	
		self._shell._verbosity = shell._verbosity
		
		args.pop( 0 )
		self._shell.run( args )
		
		return 0
		
		
	def autocomplete( self, shell, args ):
	
		choices = []
		return choices


class Shell(shell.Shell):
	
	def __init__( self, verbosity=1 ):
		shell.Shell.__init__( self, title="hop", verbosity=verbosity )
		self.add_command( List() )
		self.add_command( Info() )
		

class List(commands.Command):

	def __init__( self ):
		commands.Command.__init__( self, "list" )
		
		
	def run( self, shell, args ):
	
		hops = Hop.list_hops()
		
		for hop in hops:
			shell.print( "%s (%saa)" % ( hop.name, hop.alpha_acids ), lpad=1 )
			
		return 0
		
		
	def autocomplete( self, shell, args ):
	
		choices = []	
		return choices


class Info(commands.Command):

	def __init__( self ):
		commands.Command.__init__( self, "info" )
		
		
	def run( self, shell, args ):
	
		if len(args) <= 1:
			shell.error( Language.get( Info, "please_specify_hop" ) )
			
		else:
			args.pop( 0 )
			hop_name = " ".join( args )
			hop = Hop.get( hop_name )
			
			if hop:
				title = Language.get( Info, "hop_variety" ) % hop.name
				shell.print( title, lpad=1 )
				shell.print( "=" * len(title), lpad=1 )
				shell.print( "" )
				
				shell.print( hop.description, lpad=1 )
				shell.print( "" )
				
				left_length = 0
				keys = {
					"purpose": "purpose",
					"alpha_acids": "alpha_acids",
					"cohumulone": "cohumulone",
					"beta_acids": "beta_acids",
					"humulene": "_humulene_oil",
					"myrcene": "_myrcene_oil",
					"caryophyllene": "_caryophyllene_oil",
					"farnesene": "_farnesene_oil",
					"oil_per_100g": "_oil_volume_per_100g",
					"aliases": "aliases",
					"country": "country",
					"characteristics": "characteristics",
					"styles": "styles",
					"substitutes": "substitutes"
				}
				
				for key in keys:
					if keys[key] in hop.__dict__ and hop.__dict__[keys[key]] != None:
						will_be_printed = True
	
						if isinstance( hop.__dict__[keys[key]], list ) and len(hop.__dict__[keys[key]]) == 0:
							will_be_printed = False
						
						if will_be_printed:
							if len(Language.get( Info, key )) > left_length:
								left_length = len(Language.get( Info, key ))
				
				# Before & After spaces
				left_length += 2
				
				if hop.purpose:
					shell.print( Language.get( Info, "purpose_%s" % hop.purpose ), left_text=" %s" % Language.get( Info, "purpose" ), lpad=left_length )
				
				if hop.alpha_acids:
					shell.print( hop.alpha_acids.to_string(), left_text=" %s" % Language.get( Info, "alpha_acids" ), lpad=left_length )
				
				if hop.cohumulone:
					shell.print( hop.cohumulone.to_string(), left_text=" %s" % Language.get( Info, "cohumulone" ), lpad=left_length )
				
				if hop.beta_acids:
					shell.print( hop.beta_acids.to_string(), left_text=" %s" % Language.get( Info, "beta_acids" ), lpad=left_length )
				
				# TODO: Do not access values by protected member
				if hop._humulene_oil:
					shell.print( hop._humulene_oil.to_string(), left_text=" %s" % Language.get( Info, "humulene" ), lpad=left_length )
				
				if hop._myrcene_oil:
					shell.print( hop._myrcene_oil.to_string(), left_text=" %s" % Language.get( Info, "myrcene" ), lpad=left_length )
				
				if hop._caryophyllene_oil:
					shell.print( hop._caryophyllene_oil.to_string(), left_text=" %s" % Language.get( Info, "caryophyllene" ), lpad=left_length )
				
				if hop._farnesene_oil:
					shell.print( hop._farnesene_oil.to_string(), left_text=" %s" % Language.get( Info, "farnesene" ), lpad=left_length )
				
				if hop._oil_volume_per_100g:
					shell.print( hop._oil_volume_per_100g.to_string( unit="mL" ), left_text=" %s" % Language.get( Info, "oil_per_100g" ), lpad=left_length )
				
				shell.print( "" )
				
				if len(hop.aliases):
					shell.print( ", ".join( hop.aliases ), left_text=" %s" % Language.get( Info, "aliases" ), lpad=left_length )
				
				if hop.country:
					shell.print( hop.country_name, left_text=" %s" % Language.get( Info, "country" ), lpad=left_length )
				
				if len(hop.characteristics):
					shell.print( ", ".join( hop.characteristics ), left_text=" %s" % Language.get( Info, "characteristics" ), lpad=left_length )
				
				if len(hop.styles):
					shell.print( ", ".join( hop.styles ), left_text=" %s" % Language.get( Info, "styles" ), lpad=left_length )
				
				if len(hop.substitutes):
					shell.print( ", ".join( hop.substitutes ), left_text=" %s" % Language.get( Info, "substitutes" ), lpad=left_length )
				
				shell.print( "" )
			else:
				shell.error( Language.get( Info, "hop_does_not_exist" ) % hop_name )
			
		return 0
		
		
	def autocomplete( self, shell, args ):
	
		choices = []	
		return choices


