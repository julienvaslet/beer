# -*- coding: utf-8 -*-

import os
import sys
import errno
import configparser
import log
import re
from language import Language

class Ingredient():

	_ingredients = {}
	

	def __init__( self, config ):
	
		self._name = config["ingredient"]["name"]
		self._description = Language.get( self.__class__, "%s_description" % self.getCleanName() )
		self._aliases = []
		self._styles = []
		self._substitutes = []
		self._characteristics = []
		self._country = None
		
		if "aliases" in config["ingredient"]:
			self._aliases = re.split( r"\s*,\s*", config["ingredient"]["aliases"] )
		
		if "styles" in config["ingredient"]:
			self._styles = re.split( r"\s*,\s*", config["ingredient"]["styles"] )
		
		if "substitutes" in config["ingredient"]:
			self._substitutes = re.split( r"\s*,\s*", config["ingredient"]["substitutes"] )
			
		if "characteristics" in config["ingredient"]:
			self._characteristics = re.split( r"\s*,\s*", config["ingredient"]["characteristics"] )
		
		if "country" in config["ingredient"]:
			self._country = Language.get( Ingredient, "country_%s" % Ingredient.sanitizeName( config["ingredient"]["country"] ) )
		
		
	def getName( self ):
	
		return self._name
		
		
	def getCleanName( self ):
	
		return Ingredient.sanitizeName( self._name )
		
		
	def getCountry( self ):
		return self._country
		
		
	@classmethod
	def sanitizeName( cls, name ):
	
		return name.strip().lower()
	
		
	@classmethod
	def loadDirectory( cls, dirpath ):
		
		if os.path.abspath( dirpath ) != dirpath:
			dirpath = os.path.dirname( os.path.abspath( sys.argv[0] ) ) + os.sep + dirpath
		
		for f in os.listdir( dirpath ):
			filepath = dirpath + os.sep + f
		
			if os.path.isdir( filepath ):
				cls.loadDirectory( filepath )
				
			elif os.path.isfile( filepath ) and re.search( "\.ini$", f ):
				cls.load( filepath )
	
	
	@classmethod
	def load( cls, filepath ):
		
		if os.path.isfile( filepath ):
			config = configparser.ConfigParser()
			config.read( filepath )
			
			if "ingredient" in config:
				
				if "name" in config["ingredient"]:
					name = cls.sanitizeName( config["ingredient"]["name"] )
				
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

