# -*- coding: utf-8 -*-

from .ingredient import *

class Sugar(Ingredient):
	
	def __init__( self, config ):
	
		Ingredient.__init__( self, config )

