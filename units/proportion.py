# -*- coding: utf-8 -*-

from .unit import *

class Proportion(Unit):
	
	units = {}
	
	@property
	def numeric_value( self ):
		return self._value


class Percentage(Proportion):
	"""Percentage."""

	unit = "%"
	multiples = { "%": 1 }
	conversions = {}

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )
	
	
	@property
	def numeric_value( self ):
		return self._value / 100.0
