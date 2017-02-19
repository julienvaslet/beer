# -*- coding: utf-8 -*-

from .unit import *

class Weight(Unit):
	"""Weight unit class container.
	
	Weights are:
		- Gram: g (kg, mg)
		- Pound: lb (oz)
	"""

	units = {}
	

class Gram(Weight):

	unit = "g"
	multiples = { "kg": 1000, "g": 1, "mg": 0.001 }
	conversions = { "lb": lambda g: g * 0.002204623 }

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )


class Pound(Weight):

	unit = "lb"
	multiples = { "lb": 1, "oz": 0.0625 }
	conversions = { "g": lambda p: p * 453.59237 }

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )

