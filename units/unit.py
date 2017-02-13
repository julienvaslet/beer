# -*- coding: utf-8 -*-

import re

class Unit():

	units = {}

	def __init__( self, value, unit=None ):
		if unit != None and unit in self.multiples:
			value *= self.multiples[unit]
		
		self._value = value
		self._unit = self.unit
		
	
	def getValue( self, unit=None ):
		v = self._value
		
		if unit != None:
			if unit in self.multiples:
				v /= self.multiples[unit]
				
			elif unit in self.conversions:
				v /= self.conversions[unit]
				
			else:
				v = None
			
		return v
		
		
	def toString( self, unit=None ):
		v = self._value
		
		if unit != None:
			if unit in self.multiples:
				v /= self.multiples[unit]
				
				
			else:
				unitFound = False
				
				for conversionUnit in self.conversions:
					if unit == conversionUnit:				
						v /= self.conversions[conversionUnit]
						unitFound = True
						break
						
					else:
						if conversionUnit in self.units and unit in self.units[conversionUnit].multiples:
							transitionUnit = self.units[conversionUnit]( v / self.conversions[conversionUnit], unit=conversionUnit )
							v = transitionUnit.getValue( unit=unit )
							unitFound = True
							break
				
				if not unitFound or v == None:
					v = self._value
					unit = self.unit

		else:
			# TODO: find the "best" multiple to print the value
			v = v
			unit = self.unit

		# TODO: Print without useless decimals
		return "%0.3f %s" % ( round( v, 3 ), unit)


	@classmethod
	def parse( cls, text ):
		unit = None
		
		match = re.match( r"^\s*([+-]?)\s*([0-9]+(?:[.,][0-9]+)?)\s*([a-zA-Z°]+(?:/[a-zA-Z°]+)?)\s*$", text )
		
		if match:
			sign = -1.0 if match.group( 1 ) == "-" else 1.0
			value = sign * float( match.group( 2 ).replace( ",", "." ) )
			unitName = match.group( 3 )
			
			if unitName in Unit.units:
				unit = Unit.units[unitName]( value, unitName )
		
		return unit
