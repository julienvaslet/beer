# -*- coding: utf-8 -*-

from .ingredient import *
from units import *

class Hop(Ingredient):
	
	def __init__( self, config ):
	
		Ingredient.__init__( self, config )
		
		self._alpha_acid = unit.Unit.create( config["hop"]["alpha_acid"] ) if "alpha_acid" in config["hop"] else None
		self._cohumulone = unit.Unit.create( config["hop"]["cohumulone"] ) if "cohumulone" in config["hop"] else None
		self._beta_acid = unit.Unit.create( config["hop"]["beta_acid"] ) if "beta_acid" in config["hop"] else None
		
		self._humulene_oil = unit.Unit.create( config["hop"]["humulene_oil"] ) if "humulene_oil" in config["hop"] else None
		self._myrcene_oil = unit.Unit.create( config["hop"]["myrcene_oil"] ) if "myrcene_oil" in config["hop"] else None
		self._caryophyllene_oil = unit.Unit.create( config["hop"]["caryophyllene_oil"] ) if "caryophyllene_oil" in config["hop"] else None
		self._farnesene_oil = unit.Unit.create( config["hop"]["farnesene_oil"] ) if "farnesene_oil" in config["hop"] else None
		self._oil_volume_per_100g = unit.Unit.create( config["hop"]["oil_volume_per_100g"] ) if "oil_volume_per_100g" in config["hop"] else None

		self._purpose = config["hop"]["purpose"] if "purpose" in config["hop"] and config["hop"]["purpose"] in ["aroma", "bitterness", "dual"] else None
		
		# General infos
		#cone_density = Loose to moderate
		#growth_rate = Moderate
		#yield_amount = 800-1200 kg/hectare
		#seasonal_maturity = Mid
		#storability = Retains 45%-55% alpha acid after 6 monthes storage at 20 °C
		#east_of_harvest = Moderate
		#cone_size = Small to medium
		#resistant to (Language)
		#susceptible to (Language)
		
	
	def getPurpose( self ):
		return self._purpose
		
	def getAlphaAcid( self ):
		return self._alpha_acid
		
	def getCohumulone( self ):
		return self._cohumulone
		
	def getBetaAcid( self ):
		return self._beta_acid
		

