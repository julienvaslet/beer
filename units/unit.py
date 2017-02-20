# -*- coding: utf-8 -*-

import re
from collections import OrderedDict

class Unit():
	"""Represents an abstract unit.
	
	Represents an abstract unit ; each unit is a subclass of this class.
	
	Class variables:
		- (dict) units: (str => class) array of loaded units.
		- (dict) multiples: (str => float) array of unit multiples.
		- (dict) conversions: (str => lambda) array of unit conversions.
	
	Attributes:
		- (float) _value: The value.
		- (str) _unit: The unit of the value.
		
	"""

	units = {}

	def __init__( self, value, unit=None ):
		"""Initialize an unit."""
		
		if unit != None and unit in self.multiples:
			value *= self.multiples[unit]
		
		self._value = value
		self._unit = self.unit
		
	
	def getValue( self, unit=None ):
		"""Returns the value, in the specified unit or the default one.
		
		Returns the value, in the specified unit. If no unit is specified the
		default one is used. If the asked conversion is unavailable, None is
		returned.
		
		Parameters:
			- (str) unit: The unit in which to convert the value (default: None).
			
		Return value:
			- (float) -- the converted value.
			
			If the asked conversion is unavailable, None is returned.
		"""
		
		v = self._value
		
		if unit != None:
			if unit in self.multiples:
				v /= self.multiples[unit]
				
			else:
				unitFound = False
				
				for conversionUnit in self.conversions:
					if unit == conversionUnit:				
						v = self.conversions[conversionUnit]( v )
						unitFound = True
						break
						
					else:
						if conversionUnit in self.units and unit in self.units[conversionUnit].multiples:
							transitionUnit = Unit.units[conversionUnit]( self.conversions[conversionUnit]( v ), unit=conversionUnit )
							v = transitionUnit.getValue( unit=unit )
							unitFound = True
							break
							
				if not unitFound:
					v = None
		
		return v
	
	
	def getConversionUnits( self ):
		"""Returns the available units for conversion.
		
		Return value:
			- list -- the available units for conversion.
		"""
	
		units = []
		
		for multiple in self.multiples:
			units.append( multiple )
			
		for conversionUnit in self.conversions:
			if conversionUnit in Unit.units:
				for multiple in Unit.units[conversionUnit].multiples:
					units.append( multiple )
		
		return units
	
		
	def getBestUnit( self ):
		"""Returns the proper unit to print the value.
		
		Return value:
			- str -- the proper unit for the value.
		"""
		
		return self.unit
		
	
	def toString( self, unit=None, decompose=False ):
		"""Returns the unit, converted, in string format post-fixed by the unit.
		
		Parameters:
			- (str) unit: The unit in which to convert the value (default: None).
			- (bool) decompose: The output is decomposed in unit's multiples.
		
		Return value:
			- str -- the unit converted, in string format.
		"""
		
		value = self._value
		
		if unit != None:
			value = self.getValue( unit=unit )
			
			if value == None:
				value = self._value
				unit = self.unit
		
		elif not decompose:
			unit = self.getBestUnit()
			value /= self.multiples[unit]
		
		else:
			unit = self._unit
			
		if not decompose:
			return "%s %s" % ( Unit.formatValue( value ), unit )
			
		else:
			values = []
			lastUnit = ""
			
			multiples = OrderedDict( sorted( Unit.units[unit].multiples.items(), key=lambda k: k[1], reverse=True ) )
			
			# Get the value in the smallest unit
			for multiple in multiples:
				lastUnit = multiple
			
			value = self.getValue( unit=lastUnit )
			
			# Update multiples factors
			for multiple in multiples:
				if multiple != lastUnit:
					multiples[multiple] /= multiples[lastUnit]
					
			multiples[lastUnit] = 1.0
			
			# Decompose value
			for multiple in multiples:
				multipleValue = 0
				
				while value >= multiples[multiple]:
					multipleValue += 1
					value -= multiples[multiple]
				
				if multipleValue > 0:
					values.append( "%s %s" % ( Unit.formatValue( multipleValue ), multiple ) )
			
			if len(values) > 0:
				return " ".join( values )
				
			else:
				return "0 %s" % lastUnit


	def __repr__( self ):
		return self.toString()
		
	
	def __str__( self ):
		return self.toString()
		

	@classmethod
	def parse( cls, text ):
		"""Parses a string representation of a unit into a tuple (float, str).
		
		Return value:
			- float -- the number part of the string.
			- str -- the unit part of the string.
		"""
		
		elements = None
		match = re.match( r"^\s*([+-]?)\s*([0-9]+(?:[.,][0-9]+)?)\s*([a-zA-Z°%]+(?:/[a-zA-Z°%]+)?)\s*$", text )
		
		if match:
			sign = -1.0 if match.group( 1 ) == "-" else 1.0
			elements = ( sign * float( match.group( 2 ).replace( ",", "." ) ), match.group( 3 ) )
		
		return elements
		
	
	@classmethod
	def formatValue( cls, value ):
		"""Convert a float to a standardized string."""
	
		return re.sub( r"\.?0+$", "", "%0.3f" % round( value, 3 ) )
		

	@classmethod
	def create( cls, text ):
		"""Creates an Unit from a string representation.
		
		Creates an Unit from a string representation. The unit subclass is used
		for the creation from `Unit.units` dict.
		
		Return value:
			- Unit -- the parsed unit.
		"""
	
		unit = None
		
		elements = cls.parse( text )
		
		if elements != None:
			if elements[1] in Unit.units:
				unit = Unit.units[elements[1]]( elements[0], elements[1] )
		
		return unit
		
		
	@classmethod
	def getAllUnits( cls ):
		"""Returns the list of all loaded units.
		
		Return value:
			- list -- the list of all units.
		"""
		
		return cls.units.keys()

