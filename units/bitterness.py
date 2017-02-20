# -*- coding: utf-8 -*-

from .unit import *

class Bitterness(Unit):
	"""Bitterness unit class container."""

	units = {}
	

class AcidAlphaUnit(Bitterness):

	unit = "AAU"
	multiples = { "AAU": 1 }
	conversions = {}

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )

