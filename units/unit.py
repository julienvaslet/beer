# -*- coding: utf-8 -*-

import re
import numbers
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
		
	
	def get_value( self, unit=None ):
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
				unit_found = False
				
				for conversion_unit in self.conversions:
					if unit == conversion_unit:				
						v = self.conversions[conversion_unit]( v )
						unit_found = True
						break
						
					else:
						if conversion_unit in self.units and unit in self.units[conversion_unit].multiples:
							transition_unit = Unit.units[conversion_unit]( self.conversions[conversion_unit]( v ), unit=conversion_unit )
							v = transition_unit.get_value( unit=unit )
							unit_found = True
							break
							
				if not unit_found:
					v = None
		
		return v
	
	@property
	def conversion_units( self ):
		"""Returns the available units for conversion.
		
		Return value:
			- list -- the available units for conversion.
		"""
	
		units = []
		
		for multiple in self.multiples:
			units.append( multiple )
			
		for conversion_unit in self.conversions:
			if conversion_unit in Unit.units:
				for multiple in Unit.units[conversion_unit].multiples:
					units.append( multiple )
		
		return units
	
	
	@property
	def best_unit( self ):
		"""Returns the proper unit to print the value.
		
		Return value:
			- str -- the proper unit for the value.
		"""
		
		return self.unit
		
	
	def to_string( self, unit=None, decompose=False ):
		"""Returns the unit, converted, in string format post-fixed by the unit.
		
		Parameters:
			- (str) unit: The unit in which to convert the value (default: None).
			- (bool) decompose: The output is decomposed in unit's multiples.
		
		Return value:
			- str -- the unit converted, in string format.
		"""
		
		value = self._value
		
		if unit != None:
			value = self.get_value( unit=unit )
			
			if value == None:
				value = self._value
				unit = self.unit
		
		elif not decompose:
			unit = self.best_unit
			value /= self.multiples[unit]
		
		else:
			unit = self._unit
			
		if not decompose:
			return "%s %s" % ( Unit.format_value( value ), unit )
			
		else:
			values = []
			last_unit = ""
			
			multiples = OrderedDict( sorted( Unit.units[unit].multiples.items(), key=lambda k: k[1], reverse=True ) )
			
			# Get the value in the smallest unit
			for multiple in multiples:
				last_unit = multiple
			
			value = self.get_value( unit=last_unit )
			
			# Update multiples factors
			for multiple in multiples:
				if multiple != last_unit:
					multiples[multiple] /= multiples[last_unit]
					
			multiples[last_unit] = 1.0
			
			# Decompose value
			for multiple in multiples:
				multiple_value = 0
				
				while value >= multiples[multiple]:
					multiple_value += 1
					value -= multiples[multiple]
				
				if multiple_value > 0:
					values.append( "%s %s" % ( Unit.format_value( multiple_value ), multiple ) )
			
			if len(values) > 0:
				return " ".join( values )
				
			else:
				return "0 %s" % last_unit


	def __repr__( self ):
		return self.to_string()
		
	
	def __str__( self ):
		return self.to_string()
		
	
	def __imul__( self, value ):
		from .proportion import Proportion
	
		if isinstance( value, numbers.Real ):
			self._value *= value
		
		elif isinstance( value, Proportion ):
			self._value *= value.numeric_value
		
		else:
			raise NotImplementedError()
		
		return self
	
	
	def __mul__( self, value ):
		copy = self.copy()
		copy *= value
		
		return copy
	
	
	def __rmul__( self, value ):
		copy = self.copy()
		copy *= value
		
		return copy
		
	
	def __itruediv__( self, value ):
		if isinstance( value, numbers.Real ):
			self._value /= value
		
		else:
			raise NotImplementedError()
		
		return self
	
	
	def __truediv__( self, value ):
		copy = None
	
		if isinstance( value, numbers.Real ):
			copy = self.copy()
			copy /= value
		
		elif isinstance( value, self.__class__ ):
			copy = Unit.create( "%f %%" % ((self._value / value.get_value( unit=self._unit )) * 100) )
			
		else:
			raise NotImplementedError()
		
		return copy
	
	
	# Is it meaningless?
	def __rtruediv__( self, value ):
		copy = self.copy()
		copy /= value
		
		return copy
		
	
	def __iadd__( self, value ):
		from .proportion import Proportion
		
		if isinstance( value, self.__class__ ):
			self._value += value
		
		elif isinstance( value, Proportion ):
			self._value += self._value * value.numeric_value
		
		else:
			raise NotImplementedError()
		
		return self
	
	
	def __add__( self, value ):
		copy = self.copy()
		copy += value
		
		return copy
	
	
	def __radd__( self, value ):
		copy = self.copy()
		copy += value
		
		return copy
		
	
	def __isub__( self, value ):
		from .proportion import Proportion
		
		if isinstance( value, self.__class__ ):
			self._value -= value._value
			
		elif isinstance( value, Proportion ):
			self._value -= self._value * value.numeric_value
		
		else:
			raise NotImplementedError()
		
		return self
	
	
	def __sub__( self, value ):
		copy = self.copy()
		copy -= value
		
		return copy
	
	
	def __rsub__( self, value ):
		copy = self.copy()
		copy += -1 * value
		
		return copy
	
	
	def copy( self ):
		return self.__class__( self._value, unit=self._unit )


	@classmethod
	def parse( cls, text ):
		"""Parses a string representation of a unit into a tuple (float, str [, float]).
		
		Return value:
			- float -- the number part of the string or the lower value or the range.
			- str -- the unit part of the string.
			- float -- the higher value of the range.
		"""
		
		elements = None
		match = re.match( r"^\s*([+-]?)\s*([0-9]+(?:[.,][0-9]+)?)(?:\s*~\s*([+-]?)\s*([0-9]+(?:[.,][0-9]+)?))?\s*([a-zA-Z°%]+(?:/[a-zA-Z°%]+)?)\s*$", text )
		
		if match:
			lsign = -1.0 if match.group( 1 ) == "-" else 1.0
			
			if match.group( 3 ) == None:
				elements = ( lsign * float( match.group( 2 ).replace( ",", "." ) ), match.group( 5 ) )
				
			else:
				hsign = -1.0 if match.group( 3 ) == "-" else 1.0
				elements = ( lsign * float( match.group( 2 ).replace( ",", "." ) ), match.group( 5 ), hsign * float( match.group( 4 ).replace( ",", "." ) ) )
		
		return elements
		
	
	@classmethod
	def format_value( cls, value ):
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
			
				if len(elements) > 2:
					unit = Range( elements[0], elements[2], elements[1] )
				else:
					unit = Unit.units[elements[1]]( elements[0], unit=elements[1] )
		
		return unit
		
		
	@classmethod
	def get_all_units( cls ):
		"""Returns the list of all loaded units.
		
		Return value:
			- list -- the list of all units.
		"""
		
		return list(cls.units.keys())
		
		
class Range(Unit):

	def __init__( self, min_value, max_value, unit ):
		
		self._min = Unit.units[unit]( min_value, unit=unit )
		self._max = Unit.units[unit]( max_value, unit=unit )
		self._unit = self._min._unit
		self._value = self.get_value()
		
		
	#TODO: Should keep?
	def get_min( self ):
		return self._min
		
		
	#TODO: Should keep?
	def get_max( self ):
		return self._max
		
		
	def get_value( self, unit=None ):
		return (self._min.get_value( unit=unit ) + self._max.get_value( unit=unit )) / 2.0
		
		
	def to_string( self, unit=None, decompose=False ):
		return "%s ~ %s" % ( Unit.format_value( self._min.get_value( unit=unit ) ), self._max.to_string( unit=unit ) )
		
	
	@property
	def best_unit( self ):
		return self._min.best_unit


	@property
	def conversion_units( self ):
		return self._min.conversion_units
		
		
	def copy( self ):
		return self.__class__( self._min._value, self._max._value, self._unit )
		
		
	def __imul__( self, value ):
		self._min *= value
		self._max *= value
		self._value = self.get_value()
		
		return self
		
		
	def __iadd__( self, value ):
		self._min += value
		self._max += value
		self._value = self.get_value()
		
		return self
	
	
	def __isub__( self, value ):
		self._min -= value
		self._max -= value
		self._value = self.get_value()
		
		return self
	
	
	def __itruediv__( self, value ):
		self._min /= value
		self._max /= value
		self._value = self.get_value()
		
		return self

