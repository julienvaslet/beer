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
		units = []
		
		for multiple in self.multiples:
			units.append( multiple )
			
		for conversionUnit in self.conversions:
			if conversionUnit in Unit.units:
				for multiple in Unit.units[conversionUnit].multiples:
					units.append( multiple )
		
		return units
	
		
	def getBestUnit( self ):
		return self.unit
		
		
	def toString( self, unit=None ):
		v = self._value
		
		if unit != None:
			v = self.getValue( unit=unit )
			
			if v == None:
				v = self._value
				unit = self.unit
		
		else:
			unit = self.getBestUnit()
			v /= self.multiples[unit]

		# TODO: Print without useless decimals
		return "%0.3f %s" % ( round( v, 3 ), unit )


	def __repr__( self ):
		return self.toString()
		
	
	def __str__( self ):
		return self.toString()
		

	@classmethod
	def parse( cls, text ):
		
		elements = None
		match = re.match( r"^\s*([+-]?)\s*([0-9]+(?:[.,][0-9]+)?)\s*([a-zA-Z°]+(?:/[a-zA-Z°]+)?)\s*$", text )
		
		if match:
			sign = -1.0 if match.group( 1 ) == "-" else 1.0
			elements = ( sign * float( match.group( 2 ).replace( ",", "." ) ), match.group( 3 ) )
		
		return elements
		

	@classmethod
	def create( cls, text ):
		unit = None
		
		elements = cls.parse( text )
		
		if elements != None:
			if elements[1] in Unit.units:
				unit = Unit.units[elements[1]]( elements[0], elements[1] )
		
		return unit
