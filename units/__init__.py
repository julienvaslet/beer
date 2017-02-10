# -*- coding: utf-8 -*-
__all__ = [ "unit", "weight" ]

from .unit import *
from .weight import *

# Do the magic
for unitClass in Unit.__subclasses__():
	Unit.units[unitClass.unit] = unitClass
	
	for multiple in unitClass.multiples:
		Unit.units[multiple] = unitClass
		
