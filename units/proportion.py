# -*- coding: utf-8 -*-

from .unit import *

class Proportion(Unit):
	
	units = {}

class Percentage(Proportion):
	"""Percentage."""

	unit = "%"
	multiples = { "%": 1 }
	conversions = {}

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )
	

