# -*- coding: utf-8 -*-
from shell import *
from brewery.ingredients.hop import Hop
from language import Language
from units import *

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
		args.pop( 0 )
		
		if len(args) == 1:
			for cmd in self._shell._commands:
				if cmd in ["quit", "exit", "help"]:
					continue
			
				if cmd[:len(args[0])] == args[0]:
					choices.append( cmd )
					
		else:
			command = self._shell.get_command( args[0] )
			
			if command != None:
				choices = command.autocomplete( self._shell, args )
		
		return choices


class Shell(shell.Shell):
	
	def __init__( self, verbosity=1 ):
		shell.Shell.__init__( self, title="hop", verbosity=verbosity )
		self.add_command( List() )
		self.add_command( Info() )
		

class List(commands.Command):

	_options = {
		"name": { "params": -1, "default": None },
		"aroma": { "params": 0, "default": False },
		"bitterness": { "params": 0, "default": False },
		"dual": { "params": 0, "default": False },
		"country": { "params": -1, "default": None },
		"style": { "params": -1, "default": None },
		"sort": { "params": 1, "default": None },
		"limit": { "params": 1, "default": None }
	}

	def __init__( self ):
		commands.Command.__init__( self, "list" )
		
		
	def run( self, shell, args ):
	
		options = List.parse_options( args )

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
				

				if hop.humulene:
					humulene_text = hop.humulene.to_string()
					humulene_volume = hop.get_humulene_volume()
					
					if humulene_volume != None:
						humulene_text += " (%s/100 g)" % humulene_volume.to_string( "mL" )
					
					shell.print( humulene_text, left_text=" %s" % Language.get( Info, "humulene" ), lpad=left_length )
				
				if hop.myrcene:
					myrcene_text = hop.myrcene.to_string()
					myrcene_volume = hop.get_myrcene_volume()
					
					if myrcene_volume != None:
						myrcene_text += " (%s/100 g)" % myrcene_volume.to_string( "mL" )
						
					shell.print( myrcene_text, left_text=" %s" % Language.get( Info, "myrcene" ), lpad=left_length )
				
				if hop.caryophyllene:
					caryophyllene_text = hop.caryophyllene.to_string()
					caryophyllene_volume = hop.get_caryophyllene_volume()
					
					if caryophyllene_volume != None:
						caryophyllene_text += " (%s/100 g)" % caryophyllene_volume.to_string( "mL" )
						
					shell.print( caryophyllene_text, left_text=" %s" % Language.get( Info, "caryophyllene" ), lpad=left_length )
				
				if hop.farnesene:
					farnesene_text = hop.farnesene.to_string()
					farnesene_volume = hop.get_farnesene_volume()
					
					if farnesene_volume != None:
						farnesene_text += " (%s/100 g)" % farnesene_volume.to_string( "mL" )
						
					shell.print( farnesene_text, left_text=" %s" % Language.get( Info, "farnesene" ), lpad=left_length )
				
				if hop.oil_volume_per_100g:
					shell.print( hop.oil_volume_per_100g.to_string( unit="mL" ), left_text=" %s" % Language.get( Info, "oil_per_100g" ), lpad=left_length )
				
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
	
		args.pop( 0 )
		hop_name = " ".join( args )
		
		if len(hop_name):
			for hop in Hop.list_hops():
				if hop.name[:len(hop_name)].lower() == hop_name.lower():
					choices.append( hop.name )
		
		return choices


