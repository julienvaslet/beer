# -*- coding: utf-8 -*-
__all__ = [ "unit", "weight", "volume", "temperature" ]

from .unit import *
from .weight import *
from .volume import *
from .temperature import *

def _load_units( cls ):
	"""Recursively loads all subclasses of Unit into *.units class variables."""
	
	for unitClass in cls.__subclasses__():
		_autoload_units( unitClass )
		
		# If the class is an Unit
		if "unit" in unitClass.__dict__:
			cls.units[unitClass.unit] = unitClass
			
			for multiple in unitClass.multiples:
				cls.units[multiple] = unitClass
		
		# If the class is an Unit-container it is merged with its parent
		elif "units" in unitClass.__dict__:
			cls.units = { **cls.units, **unitClass.units }


# Recursively load all units
_load_units( Unit )
