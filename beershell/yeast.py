# -*- coding: utf-8 -*-
from shell import *
from brewery.ingredients.yeast import Yeast
from brewery.ingredients.ingredient import Ingredient
from language import Language
from units import *

import re

class Command(commands.Command):

	def __init__( self ):
		commands.Command.__init__( self, "yeast" )
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
		shell.Shell.__init__( self, title="yeast", verbosity=verbosity )
		self.add_command( List() )
		self.add_command( Info() )
		

class List(commands.Command):

	_options = {
		"name": { "params": -1, "default": None },
		"dry": { "params": 0, "default": False },
		"liquid": { "params": 0, "default": False },
		"attenuation": { "params": -1, "default": None },
		"style": { "params": -1, "default": None },
		"sort": { "params": 1, "default": None },
		"limit": { "params": 1, "default": None }
	}

	def __init__( self ):
		commands.Command.__init__( self, "list" )
		
		
	def run( self, shell, args ):
	
		options = List.parse_options( args )

		yeasts = Yeast.list_yeasts()	
		
		printed_yeasts = 0
		
		if options["attenuation"] and len(options["attenuation"]):
			percent = unit.Unit.create( options["attenuation"] )
			
			if isinstance( percent, proportion.Proportion ) or (isinstance( percent, unit.Range ) and isinstance( percent.get_min(), proportion.Proportion )):
				options["attenuation"] = percent
				
			else:
				shell.error( Language.get( List, "not_an_attenuation_percent" ) )
				options["attenuation"] = None
				
				return 1

		for yeast in yeasts:
			match_options = True
			
			# Name filter
			if match_options and (options["name"] and len(options["name"])):
			
				if options["name"].lower() not in yeast.name.lower():
					match_options = False
			
			# Form filter
			if match_options and (options["dry"] or options["liquid"]):
				
				match_options = False
				
				if options["dry"] and yeast.is_dry():
					match_options = True
					
				if options["liquid"] and yeast.is_liquid():
					match_options = True
					
			# Style filter
			# TODO: compare language names and aliases.
			if match_options and (options["style"] and len(options["style"])):
				
				match_options = False
				
				for style in yeast.styles:
					if Ingredient.sanitize_name( options["style"] ) == Ingredient.sanitize_name( style ):
						match_options = True
						break
			
			# Attenuation filter
			if match_options and options["attenuation"]:
				match_options = (options["attenuation"] == yeast.attenuation)
			
			if match_options:
				shell.print( "%s" % yeast.name, lpad=1 )
				printed_yeasts += 1
			
		if printed_yeasts > 0:
			shell.log( Language.get( List, "n_yeasts_listed" ) % printed_yeasts, level=0 )
		else:
			shell.log( Language.get( List, "no_yeast_found" ), level=0 )
			
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
					
			if last_option[0] == "style":
				a = 1
			
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
			shell.error( Language.get( Info, "please_specify_yeast" ) )
			
		else:
			args.pop( 0 )
			yeast_name = " ".join( args )
			yeast = Yeast.get( yeast_name )
			
			if yeast:
				title = yeast.name
				shell.print( title, lpad=1 )
				shell.print( "=" * len(title), lpad=1 )
				shell.print( "" )
				
				shell.print( yeast.description, lpad=1 )
				shell.print( "" )
				
				left_length = 0
				keys = {
					"form": "form",
					"strain": "strain",
					"attenuation": "attenuation",
					"alcohol_tolerance": "alcohol_tolerance",
					"temperature": "temperature",
					"flocculation": "flocculation",
					"pitching_rate": "pitching_rate",
					"aliases": "aliases",
					"characteristics": "characteristics",
					"styles": "styles",
					"substitutes": "substitutes"
				}
				
				for key in keys:
					if keys[key] in yeast.__dict__ and yeast.__dict__[keys[key]] != None:
						will_be_printed = True
	
						if isinstance( yeast.__dict__[keys[key]], list ) and len(yeast.__dict__[keys[key]]) == 0:
							will_be_printed = False
						
						if will_be_printed:
							if len(Language.get( Info, key )) > left_length:
								left_length = len(Language.get( Info, key ))
				
				# Before & After spaces
				left_length += 2
				
				if yeast.form:
					shell.print( Language.get( Info, "form_%s" % yeast.form ), left_text=" %s" % Language.get( Info, "form" ), lpad=left_length )
				
				if yeast.strain:
					shell.print( yeast.strain, left_text=" %s" % Language.get( Info, "strain" ), lpad=left_length )
					
				if yeast.attenuation:
					shell.print( yeast.attenuation.to_string(), left_text=" %s" % Language.get( Info, "attenuation" ), lpad=left_length )
					
				if yeast.temperature:
					shell.print( yeast.temperature.to_string( unit="°C" ), left_text=" %s" % Language.get( Info, "temperature" ), lpad=left_length )
					
				if yeast.alcohol_tolerance:
					shell.print( yeast.alcohol_tolerance.to_string(), left_text=" %s" % Language.get( Info, "alcohol_tolerance" ), lpad=left_length )
				
				if yeast.dry_weight:
					shell.print( yeast.dry_weight.to_string(), left_text=" %s" % Language.get( Info, "dry_weight" ), lpad=left_length )
				
				if yeast.flocculation:
					shell.print( yeast.flocculation, left_text=" %s" % Language.get( Info, "flocculation" ), lpad=left_length )
					
				if yeast.pitching_rate:
					shell.print( yeast.pitching_rate, left_text=" %s" % Language.get( Info, "pitching_rate" ), lpad=left_length )
				
				if len(yeast.aliases):
					shell.print( ", ".join( yeast.aliases ), left_text=" %s" % Language.get( Info, "aliases" ), lpad=left_length )
				
				if len(yeast.characteristics):
					shell.print( ", ".join( yeast.characteristics ), left_text=" %s" % Language.get( Info, "characteristics" ), lpad=left_length )
				
				if len(yeast.styles):
					shell.print( ", ".join( yeast.styles ), left_text=" %s" % Language.get( Info, "styles" ), lpad=left_length )
				
				if len(yeast.substitutes):
					shell.print( ", ".join( yeast.substitutes ), left_text=" %s" % Language.get( Info, "substitutes" ), lpad=left_length )
				
				shell.print( "" )
			else:
				shell.error( Language.get( Info, "yeast_does_not_exist" ) % yeast_name )
			
		return 0
		
		
	def autocomplete( self, shell, args ):
	
		choices = []
	
		args.pop( 0 )
		yeast_name = " ".join( args )
		
		if len(yeast_name):
			for yeast in Yeast.list_yeasts():
				if yeast.name[:len(yeast_name)].lower() == yeast_name.lower():
					choices.append( yeast.name )
		
		return choices


