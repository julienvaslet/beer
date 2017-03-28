# -*- coding: utf-8 -*-
from shell import *
from brewery.ingredients.hop import Hop
from brewery.ingredients.ingredient import Ingredient
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
		"bittering": { "params": 0, "default": False },
		"dual": { "params": 0, "default": False },
		"alpha_acids": { "params": -1, "default": None },
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
		
		printed_hops = 0
		
		if options["alpha_acids"] and len(options["alpha_acids"]):
			comparator = "eq"
			
			if options["alpha_acids"][0] in [ ">", "<" ]:
				if options["alpha_acids"][0] == "<":
					comparator = "lt"
				
				elif options["alpha_acids"][0] == ">":
					comparator = "gt"
					
				options["alpha_acids"] = options["alpha_acids"][1:]
				
			percent = unit.Unit.create( options["alpha_acids"] )
			
			if isinstance( percent, proportion.Proportion ) or (isinstance( percent, unit.Range ) and isinstance( percent.get_min(), proportion.Proportion )):
				options["alpha_acids"] = ( comparator, percent )
				
			else:
				shell.error( Language.get( List, "not_an_alpha_acids_percent" ) )
				options["alpha_acids"] = None
				
				return 1

		for hop in hops:
			match_options = True
			
			# Name filter
			if match_options and (options["name"] and len(options["name"])):
			
				if options["name"].lower() not in hop.name.lower():
					match_options = False
			
			# Purpose filter
			if match_options and (options["aroma"] or options["bittering"] or options["dual"]):
				
				match_options = False
				
				if options["aroma"] and hop.purpose == "aroma":
					match_options = True
					
				if options["bittering"] and hop.purpose == "bittering":
					match_options = True
					
				if options["dual"] and hop.purpose == "dual":
					match_options = True
			
			# Country filter
			# TODO: compare language names and aliases.
			if match_options and (options["country"] and len(options["country"])):
				
				if Ingredient.sanitize_name( options["country"] ) != Ingredient.sanitize_name( hop.country ):
					match_options = False
					
			# Style filter
			# TODO: compare language names and aliases.
			if match_options and (options["style"] and len(options["style"])):
				
				match_options = False
				
				for style in hop.styles:
					if Ingredient.sanitize_name( options["style"] ) == Ingredient.sanitize_name( style ):
						match_options = True
						break
						
			# Alpha acids filter
			if match_options and options["alpha_acids"]:
			
				comparator, percent = options["alpha_acids"]
				
				if comparator == "eq" and percent != hop.alpha_acids:
					match_options = False
					
				elif comparator == "lt" and percent <= hop.alpha_acids:
					match_options = False
					
				elif comparator == "gt" and percent >= hop.alpha_acids:
					match_options = False
			
			if match_options:
				shell.print( "%s (%saa)" % ( hop.name, hop.alpha_acids ), lpad=1 )
				printed_hops += 1	
			
		if printed_hops > 0:
			shell.log( Language.get( List, "n_hops_listed" ) % printed_hops, level=0 )
		else:
			shell.log( Language.get( List, "no_hops_found" ), level=0 )
			
		return 0
		
		
	def autocomplete( self, shell, args ):
	
		choices = []
		options = List.parse_options_as_array( args, silent=True )
		last_option = options[len(options) - 1]
		defined_options = []
		
		for option in options:
			if isinstance(option, tuple):
				defined_options.append( option[0] )
		
		# Specific option autocompletion
		if isinstance(last_option, tuple):
		
			if last_option[0] == "country":
				a = 1
			
			elif last_option[0] == "style":
				a = 1
			
			# No autocompletion on alpha_acids 
			#elif last_option[0] == "alpha_acids":
			
			# No autocompletion on --name
			#elif last_option[0] == "name":

			
			elif last_option[0] == "sort":
				a = 1
			
			elif last_option[0] == "limit":
				a = 1
		
		# New option
		elif isinstance(last_option, str):
			match = re.match( r"^-(?:-([a-zA-Z0-9][a-zA-Z0-9_-]*)?)?$", last_option )
			
			if match:
				last_opt = match.group( 1 ) if match.group( 1 ) else ""
				
				for opt in self._options:
					if opt not in defined_options and (len(last_opt) == 0 or last_opt == opt[:len(last_opt)]):
						choices.append( "--%s" % opt )
		
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


