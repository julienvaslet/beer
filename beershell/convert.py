# -*- coding: utf-8 -*-
from shell import *
from units import *
from language import Language

import re

class Command(commands.Command):

	def __init__( self ):
		commands.Command.__init__( self, "convert" )
		
	
	def run( self, shell, args ):
	
		if len(args) < 2:
			shell.print( Language.get( Command, "help_message" ) % args[0], lpad=1 )
			return 1
		
		args.pop( 0 )
		s_value = args[0]
		args.pop( 0 )
		
		value = None
		elements = unit.Unit.parse( s_value )
		
		# Unit may be the next argument
		if elements == None and len(args) > 0:
			s_value += args[0]
			args.pop( 0 )

			elements = unit.Unit.parse( s_value )
		
		# If the value could be parsed as an handled unit
		if elements != None:
			value = unit.Unit.create( s_value )
			
			if value != None:
				to_unit = None
				in_keyword = False
			
				if len(args) > 0 and args[0] == "in":
					in_keyword = True
					args.pop( 0 )
			
				if len(args) > 0:
					to_unit = args[0]
					args.pop( 0 )
				
				if to_unit != None:
					if to_unit in unit.Unit.units:
						if to_unit in value.conversion_units:
							shell.print( value.to_string( unit=to_unit ) )
							
						else:
							shell.error( Language.get( Command, "conversion_not_implemented" ) % (elements[1], to_unit) )
							return 3
					else:
						shell.error( Language.get( Command, "unit_not_handled" ) % to_unit )
						return 2
				
				elif not in_keyword:
					for to_unit in value.conversion_units:
						shell.print( value.to_string( unit=to_unit ) )
					
					# Color name special case
					if isinstance( value, color.Color ):
						shell.print( value.name )
				
				else:
					shell.error( Language.get( Command, "in_keyword_alone" ) )
					return 1
			
			else:
				shell.error( Language.get( Command, "unit_not_handled" ) % elements[1] )
				return 2
		else:
			shell.error( Language.get( Command, "it_is_not_an_unit" ) )
			return 2
		
		return 0
		
		
	def autocomplete( self, shell, args ):
	
		choices = []
		unit_as_two_args = False
	
		if len(args) > 1:
			args.pop( 0 )
		
			s_value = args[0]
			args.pop( 0 )
			elements = unit.Unit.parse( s_value )
		
			# Unit may be the next argument
			if elements == None:
				if len(args) > 0:
					unit_as_two_args = True
					s_value += args[0]
					args.pop( 0 )

					elements = unit.Unit.parse( s_value )
				
				# No unit specified
				elif re.search( r"^[+-]?[0-9]+(?:[\.,][0-9]+)?$", s_value ):
					choices = unit.Unit.get_all_units()
		
			# If the value could be parsed as an handled unit
			if elements != None:
				value = unit.Unit.create( s_value )
				incomplete_unit = False
				
				if value != None:
					if len(args) == 1 and args[0] == "in"[:len(args[0])]:
						choices.append( "in" )
					
					elif len(args) > 1:
						if args[0] == "in":
							args.pop( 0 )
						
							if len(args) == 1:
								to_unit = args[0]
							
								for conversion_unit in value.conversion_units:
									if conversion_unit[:len(to_unit)].lower() == to_unit.lower():
										choices.append( conversion_unit )
					
					else:
						incomplete_unit = True
				
				else:
					incomplete_unit = True
				
				# Incomplete unit					
				if incomplete_unit:
					for u in unit.Unit.get_all_units():
						if u[:len(elements[1])].lower() == elements[1].lower():
							if unit_as_two_args:
								choices.append( u )
							else:
								choices.append( "%s%s" % (unit.Unit.format_value( elements[0] ),u) )
		
		return choices
	
