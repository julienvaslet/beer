# -*- coding: utf-8 -*-
from shell import *
from units import *
from language import Language

import re

class ConvertCommand(command.Command):

	def __init__( self ):
		command.Command.__init__( self, "convert" )
		
	
	def run( self, shell, args ):
	
		if len(args) < 2:
			shell.print( Language.get( ConvertCommand, "help_message" ) % args[0], lpad=1 )
			return 1
		
		args.pop( 0 )
		sValue = args[0]
		args.pop( 0 )
		
		value = None
		elements = unit.Unit.parse( sValue )
		
		# Unit may be the next argument
		if elements == None and len(args) > 0:
			sValue += args[0]
			args.pop( 0 )

			elements = unit.Unit.parse( sValue )
		
		# If the value could be parsed as an handled unit
		if elements != None:
			value = unit.Unit.create( sValue )
			
			if value != None:
				toUnit = None
				inKeyword = False
			
				if len(args) > 0 and args[0] == "in":
					inKeyword = True
					args.pop( 0 )
			
				if len(args) > 0:
					toUnit = args[0]
					args.pop( 0 )
				
				if toUnit != None:
					if toUnit in unit.Unit.units:
						if toUnit in value.getConversionUnits():
							shell.print( value.toString( unit=toUnit ) )
							
						else:
							shell.error( Language.get( ConvertCommand, "conversion_not_implemented" ) % (elements[1], toUnit) )
							return 3
					else:
						shell.error( Language.get( ConvertCommand, "unit_not_handled" ) % toUnit )
						return 2
				
				elif not inKeyword:
					for toUnit in value.getConversionUnits():
						shell.print( value.toString( unit=toUnit ) )
					
					# Color name special case
					if isinstance( value, color.Color ):
						shell.print( value.getColorName() )
				
				else:
					shell.error( Language.get( ConvertCommand, "in_keyword_alone" ) )
					return 1
			
			else:
				shell.error( Language.get( ConvertCommand, "unit_not_handled" ) % elements[1] )
				return 2
		else:
			shell.error( Language.get( ConvertCommand, "it_is_not_an_unit" ) )
			return 2
		
		return 0
		
		
	def autocomplete( self, shell, args ):
	
		choices = []
		unitAsTwoArgs = False
	
		if len(args) > 1:
			args.pop( 0 )
		
			sValue = args[0]
			args.pop( 0 )
			elements = unit.Unit.parse( sValue )
		
			# Unit may be the next argument
			if elements == None:
				if len(args) > 0:
					unitAsTwoArgs = True
					sValue += args[0]
					args.pop( 0 )

					elements = unit.Unit.parse( sValue )
				
				# No unit specified
				elif re.search( r"^[+-]?[0-9]+(?:[\.,][0-9]+)?$", sValue ):
					choices = unit.Unit.getAllUnits()
		
			# If the value could be parsed as an handled unit
			if elements != None:
				value = unit.Unit.create( sValue )
				incompleteUnit = False
				
				if value != None:
					if len(args) == 1 and args[0] == "in"[:len(args[0])]:
						choices.append( "in" )
					
					elif len(args) > 1:
						if args[0] == "in":
							args.pop( 0 )
						
							if len(args) == 1:
								toUnit = args[0]
							
								for conversionUnit in value.getConversionUnits():
									if conversionUnit[:len(toUnit)].lower() == toUnit.lower():
										choices.append( conversionUnit )
					
					else:
						incompleteUnit = True
				
				else:
					incompleteUnit = True
				
				# Incomplete unit					
				if incompleteUnit:
					for u in unit.Unit.getAllUnits():
						if u[:len(elements[1])].lower() == elements[1].lower():
							if unitAsTwoArgs:
								choices.append( u )
							else:
								choices.append( "%s%s" % (unit.Unit.formatValue( elements[0] ),u) )
		
		return choices
	
