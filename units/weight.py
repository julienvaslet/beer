# -*- coding: utf-8 -*-

from .unit import *

# QUESTION? Make a single Weight global class?

class Kilogram(Unit):

	unit = "kg"
	multiples = { "g": 0.001, "mg": 0.000001 }
	conversions = {}

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )
		
		print( self._value )
		
		
class Ton(Unit):

	unit = "t"
	multiples = {}
	conversions = {}

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )
