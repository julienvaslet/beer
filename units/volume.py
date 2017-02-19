# -*- coding: utf-8 -*-

from .unit import *

class Volume(Unit):
	"""Volume unit class container.
	
	Volumes are:
		- Liter: L (hL, dL, cL, mL)
		- Gallon: gal (qt, pint, cup, fl-oz)
	"""

	units = {}
	

class Liter(Volume):

	unit = "L"
	multiples = { "hL": 100, "L": 1, "dL": 0.1, "cL": 0.01, "mL": 0.001 }
	conversions = { "gal": lambda l: l * 0.264172052 }

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )


class Gallon(Volume):

	unit = "gal"
	multiples = { "gal": 1, "qt": 0.25, "pint": 0.125, "cup": 0.0625, "fl-oz": 0.0078125 }
	conversions = { "L": lambda g: g * 3.785411784 }

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )

