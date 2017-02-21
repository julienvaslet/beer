# -*- coding: utf-8 -*-

from units import *

class Recipe():

	def __init__( self ):
		
		self._ingredients = []
		
		self._mashProfile = None
		self._spargeProfile = None
		self._boilProfile = None
		self._fermentationProfile = None
		self._carbonatationProfile = None
		
		self._originalGravity = Unit.create( "0SG" )
		self._finalGravity = Unit.create( "0SG" )
		self._color = Unit.create( "0EBC" )
		self._alcoholByVolume = 0
		self._bitterness = 0
		self._aromas = []
