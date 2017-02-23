# -*- coding: utf-8 -*-

from .unit import *
from language import Language

class Color(Unit):
	"""Color unit class container."""

	units = {}
	srmNames = [2,3,4,6,9,12,15,18,20,24,30,40]
	
	def getColorName( self ):
	
		srmValue = self.getValue( unit="°SRM" )
		closestSrm = Color.srmNames[0]
		
		for value in Color.srmNames:
			if srmValue >= value:
				closestSrm = value
			else:
				break
		
		return Language.get( Color, "color_%d_SRM" % closestSrm )


class EBC(Color):

	unit = "EBC"
	multiples = { "EBC": 1 }
	conversions = { "°L": lambda c: pow( ((c / 1.97) / 1.4922), 1/0.6859 ), "°SRM": lambda c: c / 1.97 }

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )


class Lovibond(Color):

	unit = "°L"
	multiples = { "°L": 1 }
	conversions = { "EBC": lambda c: (1.4922 * pow( c, 0.6859 )) * 1.97, "°SRM": lambda c: 1.4922 * pow( c, 0.6859 ) }

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )
		
		
class SRM(Color):

	unit = "°SRM"
	multiples = { "°SRM": 1 }
	conversions = { "EBC": lambda c: c * 1.97, "°L": lambda c: pow( (c / 1.4922), 1/0.6859 ) }

	def __init__( self, value, unit=None ):
		Unit.__init__( self, value, unit=unit )
		

