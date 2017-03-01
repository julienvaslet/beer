# -*- coding: utf-8 -*-
__all__ = [ "unit", "time", "color", "weight", "volume", "density", "extract", "proportion", "bitterness", "temperature" ]

from .unit import *
from .time import *
from .color import *
from .weight import *
from .volume import *
from .density import *
from .extract import *
from .proportion import *
from .bitterness import *
from .temperature import *

from language import Language

Language.load( "units.ini" )

def _load_units( cls ):
	"""Recursively loads all subclasses of Unit into *.units class variables."""
	
	for unit_cls in cls.__subclasses__():
		_load_units( unit_cls )
		
		# If the class is an Unit
		if "unit" in unit_cls.__dict__:
			cls.units[unit_cls.unit] = unit_cls
			
			for multiple in unit_cls.multiples:
				cls.units[multiple] = unit_cls
		
		# If the class is an Unit-container it is merged with its parent
		elif "units" in unit_cls.__dict__:
			cls.units = { **cls.units, **unit_cls.units }


# Recursively load all units
_load_units( Unit )
