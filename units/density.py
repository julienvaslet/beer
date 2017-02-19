# -*- coding: utf-8 -*-

from .unit import *

class Density(Unit):
	"""Density unit class container.
	
	Density are:
		- Specific gravity: SG
		- Points: points
		- Plato: °P
		- Brix: °B
	"""

	units = {}
	

class SpecificGravity(Density):

	unit = "SG"
	multiples = { "SG": 1 }
	conversions = {
		"points": lambda g: (g * 1000.0) - 1000.0,
		"°P": lambda g: (135.997 * pow( g, 3 )) - (630.272 * pow( g, 2 )) + (1111.14 * g) - 616.868,
		"°B": lambda g: (((((182.4601 * g) - 775.6821) * g) + 1262.7794) * g) - 669.5622
	}

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )


class Points(Density):

	unit = "points"
	multiples = { "points": 1 }
	conversions = {
		"SG": lambda g: ( g + 1000 ) / 1000.0,
		"°P": lambda g: SpecificGravity.conversions["°P"]( Points.conversions["SG"]( g ) ),
		"°B": lambda g: SpecificGravity.conversions["°B"]( Points.conversions["SG"]( g ) )
	}

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )


class Plato(Density):

	unit = "°P"
	multiples = { "°P": 1 }
	conversions = {
		"SG": lambda g: 1 + ( g / (258.6 - (227.1 * g / 258.2)) ),
		"points": lambda g: Plato.conversions["SG"]( g ) * 1000 - 1000.0,
		"°B": lambda g: SpecificGravity.conversions["°B"]( Plato.conversions["SG"]( g ) )
	}

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )


class Brix(Density):

	unit = "°B"
	multiples = { "°B": 1 }
	conversions = {
		"SG": lambda g: (g / (258.6 - ((g / 258.2) * 227.1))) + 1,
		"points": lambda g: Brix.conversions["SG"]( g ) * 1000 - 1000.0,
		"°P": lambda g: SpecificGravity.conversions["°P"]( Brix.conversions["SG"]( g ) )
	}

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )
		


