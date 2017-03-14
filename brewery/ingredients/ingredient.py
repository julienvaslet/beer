# -*- coding: utf-8 -*-

import os
import sys
import errno
import configparser
import log
import re
import unicodedata
from language import Language

class Ingredient():

	_ingredients = {}
	

	def __init__( self, config ):
	
		self.name = config["ingredient"]["name"]
		self.description = Language.get( self.__class__, "%s_description" % self.clean_name )
		self.aliases = []
		self.styles = []
		self.substitutes = []
		self.characteristics = []
		self.country = None
		
		if "aliases" in config["ingredient"]:
			self.aliases = list(filter(len, re.split( r"\s*,\s*", config["ingredient"]["aliases"] )))
		
		if "styles" in config["ingredient"]:
			self.styles = list(filter(len, re.split( r"\s*,\s*", config["ingredient"]["styles"] )))
		
		if "substitutes" in config["ingredient"]:
			self.substitutes = list(filter(len, re.split( r"\s*,\s*", config["ingredient"]["substitutes"] )))
			
		if "characteristics" in config["ingredient"]:
			self.characteristics = list(filter(len, re.split( r"\s*,\s*", config["ingredient"]["characteristics"] )))
		
		if "country" in config["ingredient"]:
			self.country = Ingredient.sanitize_name( config["ingredient"]["country"] )
		
		
	@property
	def country_name( self ):
		return Language.get( Ingredient, "country_%s" % self.country )
		
		
	@property
	def clean_name( self ):
		return Ingredient.sanitize_name( self.name )
		
		
	@classmethod
	def sanitize_name( cls, name ):
	
		return re.sub( r"[^a-z0-9_]", "", re.sub( r"\s+", "_", unicodedata.normalize( 'NFKD', name ).strip().lower() ) )
	
		
	@classmethod
	def load_directory( cls, dirpath ):
		
		if os.path.abspath( dirpath ) != dirpath:
			dirpath = os.path.dirname( os.path.realpath( os.path.abspath( sys.argv[0] ) ) ) + os.sep + dirpath
		
		for f in os.listdir( dirpath ):
			filepath = dirpath + os.sep + f
		
			if os.path.isdir( filepath ):
				cls.load_directory( filepath )
				
			elif os.path.isfile( filepath ) and re.search( "\.ini$", f ):
				cls.load( filepath )
	
	
	@classmethod
	def load( cls, filepath ):
		
		if os.path.isfile( filepath ):
			config = configparser.ConfigParser()
			config.read( filepath )
			
			if "ingredient" in config:
				
				if "name" in config["ingredient"]:
					name = cls.sanitize_name( config["ingredient"]["name"] )
				
				class_ = Ingredient	
				
				# Find the specific ingredient class
				if "hop" in config:
					from .hop import Hop
					class_ = Hop
					
				elif "malt" in config:
					from .malt import Malt
					class_ = Malt
					
				elif "yeast" in config:
					from .yeast import Yeast
					class_ = Yeast
					
				elif "sugar" in config:
					from .sugar import Sugar
					class_ = Sugar
					
				elif "water" in config:
					from .water import Water
					class_ = Water
				
				log.debug( "Loading %s \"%s\"..." % (class_.__name__.lower(), name) )

				#TODO: allow merge with user created ingredients
				cls._ingredients[name] = class_( config )
				
			else:
				log.error( "File \"%s\" has no \"ingredient\" section." % filepath )
			
		else:
			raise FileNotFoundError( errno.ENOENT, os.strerror(errno.ENOENT), filepath )

