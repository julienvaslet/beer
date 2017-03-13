# -*- coding: utf-8 -*-

from .ingredient import *
from units import *

class Hop(Ingredient):
	
	def __init__( self, config ):
	
		Ingredient.__init__( self, config )
		
		self.alpha_acids = unit.Unit.create( config["hop"]["alpha_acids"] ) if "alpha_acids" in config["hop"] else None
		self.cohumulone = unit.Unit.create( config["hop"]["cohumulone"] ) if "cohumulone" in config["hop"] else None
		self.beta_acids = unit.Unit.create( config["hop"]["beta_acids"] ) if "beta_acids" in config["hop"] else None
		
		self.humulene = unit.Unit.create( config["hop"]["humulene_oil"] ) if "humulene_oil" in config["hop"] else None
		self.myrcene = unit.Unit.create( config["hop"]["myrcene_oil"] ) if "myrcene_oil" in config["hop"] else None
		self.caryophyllene = unit.Unit.create( config["hop"]["caryophyllene_oil"] ) if "caryophyllene_oil" in config["hop"] else None
		self.farnesene = unit.Unit.create( config["hop"]["farnesene_oil"] ) if "farnesene_oil" in config["hop"] else None
		self.oil_volume_per_100g = unit.Unit.create( config["hop"]["oil_volume_per_100g"] ) if "oil_volume_per_100g" in config["hop"] else None

		self.purpose = config["hop"]["purpose"] if "purpose" in config["hop"] and config["hop"]["purpose"] in ["aroma", "bitterness", "dual"] else None
	
	
	def get_humulene_volume( self ):
		return None #self.humulene
		
	
	def get_myrcene_volume( self, weight=None ):
		return None #self.myrcene


	def get_caryophyllene_volume( self, weight=None ):
		return None #self.caryophyllene


	def get_farnesene_volume( self, weigth=None ):
		return None #self.farnesene
	
	
	def get_oil_volume( self, weigth=None ):
		return None #self._oil_volume_per_100g
	
	
	@classmethod
	def list_hops( cls, name=None ):
		hops = []
		
		for ingredient in cls._ingredients:

			if isinstance( cls._ingredients[ingredient], Hop ):
				hops.append( cls._ingredients[ingredient] )
	
		return sorted( hops, key=lambda h: h.name )
		
		
	@classmethod
	def get( cls, name ):
		hop = None
		sane_name = cls.sanitize_name( name )
		
		if sane_name in cls._ingredients:
			if isinstance( cls._ingredients[sane_name], Hop ):
				hop = cls._ingredients[sane_name]
		
		return hop
	
