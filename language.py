# -*- coding: utf-8 -*-

import os
import sys
import errno
import configparser

class Language():

	_instance = None

	def __init__( self, lang, path ):
		self._language = lang
		self._path = path
		self._content = {}
	
	
	@classmethod
	def initialize( cls, lang="en", path=None ):
		if path == None:
			path = os.path.dirname( os.path.abspath( sys.argv[0] ) ) + os.sep + "i18n"
			
		cls._instance = cls( lang, path )
	
	
	@classmethod
	def getInstance( cls ):
		if cls._instance == None:
			cls.initialize()
	
		return cls._instance
	
	
	@classmethod
	def getPath( cls, class_, key ):
		return class_.__module__ + "." + class_.__qualname__ + "." + key
	
	
	@classmethod
	def load( cls, filename ):
		language = cls.getInstance()
		
		if os.path.isfile( language._path + os.sep + language._language + os.sep + filename ):
			config = configparser.ConfigParser()
			config.read( language._path + os.sep + language._language + os.sep + filename )
			
			for section in config:
				for key in config[section]:
					language._content["%s.%s" % ( section, key )] = config[section][key]
			
		else:
			raise FileNotFoundError( errno.ENOENT, os.strerror(errno.ENOENT), language._path + os.sep + language._language + os.sep + filename )
	
	
	@classmethod
	def get( cls, class_, key ):
		language = cls.getInstance()
		
		if cls.getPath( class_, key ) in language._content:
			return language._content[cls.getPath( class_, key )]
		else:
			return ""
