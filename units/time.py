# -*- coding: utf-8 -*-

from .unit import *

class Time(Unit):
	"""Time unit class container.
	
	Times are:
		- Second: s (h, mn)
	"""

	units = {}
	

class Second(Time):

	unit = "s"
	multiples = { "h": 3600, "mn": 60, "s": 1 }
	conversions = {}

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )

