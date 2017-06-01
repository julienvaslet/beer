# -*- coding: utf-8 -*-

from .unit import *

class Pressure(Unit):
	"""Pressure unit class container.
	
	Pressures are:
		- Atmosphere: atm
		- Bar: bar, mbar
		- Pascal: Pa, hPa, kPa
		- PoundsPerSquareInchAbsolute: psia, psi
		- PoundsPerSquareInchGauge: psig
	"""

	units = {}
	

class Atmosphere(Pressure):

	unit = "atm"
	multiples = { "atm": 1 }
	conversions = { "bar": lambda a: a * 1.01325, "Pa": lambda a: a * 101325, "psia": lambda a: a * 14.69595, "psig": lambda a: PoundsPerSquareInchAbsolute.conversions["psig"]( Atmosphere.conversions["psia"]( a ) ) }

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )


class Bar(Pressure):

	unit = "bar"
	multiples = { "bar": 1, "mbar": 0.001 }
	conversions = { "atm": lambda b: b / 1.101325, "Pa": lambda b: b * 100000, "psia": lambda b: b * 14.50377, "psig": lambda b: PoundsPerSquareInchAbsolute.conversions["psig"]( Bar.conversions["psia"]( b ) ) }

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )
		
		
class Pascal(Pressure):

	unit = "Pa"
	multiples = { "Pa": 1, "hPa": 100, "kPa": 1000 }
	conversions = { "atm": lambda p: p / 101325, "bar": lambda p: p / 100000, "psia": lambda p: p * 0.0001450377, "psig": lambda p: PoundsPerSquareInchAbsolute.conversions["psig"]( Pascal.conversions["psia"]( p ) ) }

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )


class PoundsPerSquareInchAbsolute(Pressure):

	unit = "psia"
	multiples = { "psia": 1, "psi": 1 }
	conversions = { "atm": lambda p: p * 0.068046, "Pa": lambda p: p * 6894.8, "bar": lambda p: p * 0.068948, "psig": lambda p: p - 14.69595 }

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )


class PoundsPerSquareInchGauge(Pressure):

	unit = "psig"
	multiples = { "psig": 1 }
	conversions = {
		"psia": lambda p: p + 14.69595,
		"atm": lambda p: PoundsPerSquareInchAbsolute.conversions["atm"]( PoundsPerSquareInchGauge.conversions["psia"]( p ) ),
		"Pa": lambda p: PoundsPerSquareInchAbsolute.conversions["Pa"]( PoundsPerSquareInchGauge.conversions["psia"]( p ) ),
		"bar": lambda p: PoundsPerSquareInchAbsolute.conversions["bar"]( PoundsPerSquareInchGauge.conversions["psia"]( p ) )
	}

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )



