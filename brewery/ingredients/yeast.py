# -*- coding: utf-8 -*-

from .ingredient import *
from units import *

class Yeast(Ingredient):
	
	def __init__( self, config ):
	
		Ingredient.__init__( self, config )
		
		self.form = config["yeast"]["form"] if "form" in config["yeast"] and config["yeast"]["form"] in ["dry", "liquid"] else None
		self.strain = config["yeast"]["strain"] if "strain" in config["yeast"] else None

		if self.is_dry():
			self.dry_weight = unit.Unit.create( config["yeast"]["dry_weight"] ) if "dry_weight" in config["yeast"] else None
			self.viable_cells_per_g = config["yeast"]["viable_cells_per_g"] if "viable_cells_per_g" in config["yeast"] else None
		else:
			self.dry_weight = None
			self.viable_cells_per_g = None
		
		self.attenuation = unit.Unit.create( config["yeast"]["attenuation"] ) if "attenuation" in config["yeast"] else None
		self.alcohol_tolerance = unit.Unit.create( config["yeast"]["alcohol_tolerance"] ) if "alcohol_tolerance" in config["yeast"] else None
		self.temperature = unit.Unit.create( config["yeast"]["temperature"] ) if "temperature" in config["yeast"] else None
		self.flocculation = config["yeast"]["flocculation"] if "flocculation" in config["yeast"] else None
		self.pitching_rate = config["yeast"]["pitching_rate"] if "pitching_rate" in config["yeast"] else None


	def is_dry( self ):
		return self.form == "dry"
		
		
	def is_liquid( self ):
		return self.form == "liquid"
		
		
	@classmethod
	def list_yeasts( cls, name=None ):
		yeasts = []
		
		for ingredient in cls._ingredients:

			if isinstance( cls._ingredients[ingredient], Yeast ):
				yeasts.append( cls._ingredients[ingredient] )
	
		return sorted( yeasts, key=lambda h: h.name )
		
		
	@classmethod
	def get( cls, name ):
		yeast = None
		sane_name = cls.sanitize_name( name )
		
		if sane_name in cls._ingredients:
			if isinstance( cls._ingredients[sane_name], Yeast ):
				yeast = cls._ingredients[sane_name]
		
		return yeast

