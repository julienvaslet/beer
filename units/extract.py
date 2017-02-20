# -*- coding: utf-8 -*-

from .unit import *

class Extract(Unit):
	"""Extract unit class container.
	
	Extract are:
		- %Extract: %Extract
		- Points/Pound/Gallon: ppg
		- Hot Water Extract (kg-degrees/L): HWE
	"""

	units = {}
	

class PercentExtract(Extract):

	unit = "%Extract"
	multiples = { "%Extract": 1 }
	conversions = {
		"ppg": lambda p: 46.0 * (p / 100.0),
		"HWE": lambda p: PointsPoundGallon.conversions["HWE"]( PercentExtract.conversions["ppg"]( p ) )
	}

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )


class PointsPoundGallon(Extract):

	unit = "ppg"
	multiples = { "ppg": 1 }
	conversions = {
		"%Extract": lambda ppg: (ppg / 46.0) * 100.0,
		"HWE": lambda ppg: 8.345 * ppg
	}
		
	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )


class HotWaterExtract(Extract):

	unit = "HWE"
	multiples = { "HWE": 1 }
	conversions = {
		"%Extract": lambda h: PointsPoundGallon.conversions["%Extract"]( HotWaterExtract.conversions["ppg"]( h ) ),
		"ppg": lambda h: h / 8.345
	}

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )


