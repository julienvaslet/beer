# -*- coding: utf-8 -*-

from .unit import *

class Temperature(Unit):
	"""Temperature unit class container.
	
	Temperatures are:
		- Celsius: °C
		- Fahrenheit: °F
		- Kelvin: K
	"""

	units = {}
	

class Celsius(Temperature):

	unit = "°C"
	multiples = { "°C": 1 }
	conversions = { "°F": lambda c: (c * 9/5) + 32, "K": lambda c: c + 273.15 }

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )


class Fahrenheit(Temperature):

	unit = "°F"
	multiples = { "°F": 1 }
	conversions = { "°C": lambda f: (f - 32) * 5/9, "K": lambda f: (f + 459.67) * 5/9 }

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )
		
		
class Kelvin(Temperature):

	unit = "K"
	multiples = { "K": 1 }
	conversions = { "°C": lambda k: k - 273.15, "°F": lambda k: (k * 9/5) - 459.67 }

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )


