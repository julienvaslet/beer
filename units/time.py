# -*- coding: utf-8 -*-

from .unit import *

class Time(Unit):
	"""Time unit class container."""

	units = {}
	

class Minute(Time):

	unit = "mn"
	multiples = { "h": 60, "mn": 1, "s": 1/60 }
	conversions = {}

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )

