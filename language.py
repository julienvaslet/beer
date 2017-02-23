# -*- coding: utf-8 -*-

import os
import sys
import errno
import configparser
import log

class Language():
	"""Represents the singleton Language class which provides localized texts.
	
	Represents the singleton Language class which provides localized texts.
	Text values are stored in INI files and can be load with the `load` method.
	By default, files are located in "<app root>/i18n/<language>/" directory.
	INI's section names are part of the full key-path of a text. For instance,
	this class, Language, is fully named "language.Language". In our fictive
	INI file there will be a "language.Language" section with a key "my_text".
	To access this value, the language `get` method will be used by passing
	the class and the key: `Language.get( Language, "my_text" )`. The path-key
	will be generated as "language.Language.my_text" and will match our INI
	parsed file.
	
	Class variables:
		- (Language) _instance: the current Language instance.
	"""

	_instance = None

	def __init__( self, lang, path ):
		"""Internal Language instance initialization."""
		
		self._language = lang
		self._path = path
		self._content = {}
		self._files = set()
	
	
	@classmethod
	def initialize( cls, lang="en", path=None ):
		"""Initialize the language instance.
		
		Initialize the language instance. If the path is unspecified
		the default used path is "<app root>/i18n".
		
		Parameters:
			- lang: The language (default: "en").
			- path: The languages files location (default: None).
		"""
		
		if path == None:
			path = os.path.dirname( os.path.abspath( sys.argv[0] ) ) + os.sep + "i18n"
		
		log.debug( "Initializing language \"%s\"." % lang )
		
		if cls._instance == None:
			cls._instance = cls( lang, path )
		
		else:
			loadedFiles = cls._instance._files
			cls._instance = cls( lang, path )
			
			for filename in loadedFiles:
				cls._instance.load( filename )
	
	
	@classmethod
	def getInstance( cls ):
		"""Returns the current Language instance (initialize it if necessary)."""
		
		if cls._instance == None:
			cls.initialize()
	
		return cls._instance
	
	
	@classmethod
	def getPath( cls, class_, key ):
		"""Returns the full key-path according to class and key values."""
		
		return class_.__module__ + "." + class_.__qualname__ + "." + key.lower()
	
	
	@classmethod
	def load( cls, filename ):
		"""Loads an INI file into the Language text collection."""
		
		language = cls.getInstance()
		
		if filename not in language._files:
			if os.path.isfile( language._path + os.sep + language._language + os.sep + filename ):
				log.debug( "Loading language file: %s..." % (language._language + os.sep + filename) )
				language._files.add( filename )
			
				config = configparser.ConfigParser()
				config.read( language._path + os.sep + language._language + os.sep + filename )
			
				for section in config:
					for key in config[section]:
						language._content["%s.%s" % ( section, key )] = config[section][key]
			
			else:
				raise FileNotFoundError( errno.ENOENT, os.strerror(errno.ENOENT), language._path + os.sep + language._language + os.sep + filename )
	
	
	@classmethod
	def get( cls, class_, key ):
		"""Returns the text-value according to the specified class_ and key values.
		
		Parameters:
			- (class) class_: The class.
			- (str) key: The text key.
		"""
		
		language = cls.getInstance()
		
		if cls.getPath( class_, key ) in language._content:
			return language._content[cls.getPath( class_, key )]
		else:
			log.warn( "Text not found: %s" % cls.getPath( class_, key ), level=2 )
			return ""

