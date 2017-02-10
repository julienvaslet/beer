# -*- coding: utf-8 -*-

class Unit():

	units = {}

	def __init__( self, value, unit=None ):
		if unit != None and unit in self.multiples:
			value *= self.multiples[unit]
			
		self._value = value
