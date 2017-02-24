# -*- coding: utf-8 -*-

from .unit import *
from language import Language

class Color(Unit):
	"""Color unit class container."""

	units = {}
	srmNames = [2,3,4,6,9,12,15,18,20,24,30,40]
	
	# Functions are Lagrange interpolations from a set of predefined colors
	rgbFunctions = {
		"r": {
			"max": 80,
			"fx": lambda x: round( (-32477 * pow(x,6) / 1769040000000) + (10511 * pow(x,5) / 2268000000) - (31861909 * pow(x,4) / 70761600000) + (142540771 * pow(x,3) / 7076160000) - (36465581 * pow(x,2) / 117936000) - (57530597 * x / 8845200) + 255 )
		},
		"g": {
			"max": 38,
			"fx": lambda x: round( (-173081 * pow(x,5) / 70685214600) + (18673381 * pow(x,4) / 35342607300) - (3010761059 * pow(x,3) / 70685214600) + (58136754119 * pow(x,2) / 35342607300) - (15956116849 * x / 504894390) + 255 )
		},
		"b": {
			"max": 8.5,
			"fx": lambda x: round( (-0.00847763 * pow(x,5)) + (0.262428 * pow(x,4)) - (3.44515 * pow(x,3)) + (25.7081 * pow(x,2)) - 116.517 * x + 255 )
		}
	}
	
	
	def getColorName( self ):
	
		srmValue = self.getValue( unit="°SRM" )
		closestSrm = Color.srmNames[0]
		
		for value in Color.srmNames:
			if srmValue >= value:
				closestSrm = value
			else:
				break
		
		return Language.get( Color, "color_%d_SRM" % closestSrm )
		
		
	def getRGBColor( self ):
		srmValue = self.getValue( unit="°SRM" )
		
		r = 0 if srmValue >= Color.rgbFunctions["r"]["max"] else Color.rgbFunctions["r"]["fx"]( srmValue )
		g = 0 if srmValue >= Color.rgbFunctions["g"]["max"] else Color.rgbFunctions["g"]["fx"]( srmValue )
		b = 0 if srmValue >= Color.rgbFunctions["b"]["max"] else Color.rgbFunctions["b"]["fx"]( srmValue )
		
		return (r, g, b)


	def getHexColor( self ):
		return "#%02x%02x%02x" % self.getRGBColor()


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
		
