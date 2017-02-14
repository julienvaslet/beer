# -*- coding: utf-8 -*-
from shell import *
from units import *

class ConvertCommand(command.Command):

	def __init__( self ):
		command.Command.__init__( self, "convert", description="Converts units." )
	
	
	def run( self, shell, args ):
	
		if len(args) < 2:
			shell.print( "usage: %s <value> <unit> [[in] <unit>]" % args[0], lpad=1 )
			shell.print( "Converts value between specified units.", lpad=1 )
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
							shell.error( "Conversion from \"%s\" to \"%s\" is not implemented." % (elements[1], toUnit) )
							return 3
					else:
						shell.error( "Unit \"%s\" is not handled." % toUnit )
						return 2
				
				elif not inKeyword:
					for toUnit in value.getConversionUnits():
						shell.print( value.toString( unit=toUnit ) )
				
				else:
					shell.error( "The keyword \"in\" must be followed by an unit." )
					return 1
			
			else:
				shell.error( "Unit \"%s\" is not handled." % elements[1] )
				return 2
		else:
			shell.error( "You have typed something that is not an unit." )
			return 2
		
		return 0
		
		
	def autocomplete( self, shell, args ):
	
		choices = []
	
		if len(args) > 1:
			args.pop( 0 )
		
			sValue = args[0]
			args.pop( 0 )
			elements = unit.Unit.parse( sValue )
		
			# Unit may be the next argument
			if elements == None and len(args) > 0:
				sValue += args[0]
				args.pop( 0 )

				elements = unit.Unit.parse( sValue )
		
			# If the value could be parsed as an handled unit
			if elements != None:
				value = unit.Unit.create( sValue )
				
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
		
		return choices
	
