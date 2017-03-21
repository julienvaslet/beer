#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
import environment

from units import *

class TestUnits(unittest.TestCase):

	def test_comparison_unit_unit( self ):
		
		kg2 = unit.Unit.create( "2kg" )
		kg2b = unit.Unit.create( "2kg" )
		kg5 = unit.Unit.create( "5kg" )
		
		# Unit == Unit
		self.assertTrue( kg2 == kg2b )
		self.assertTrue( kg2b == kg2 )
		self.assertFalse( kg2 == kg5 )
		self.assertFalse( kg5 == kg2 )
		
		# Unit != Unit
		self.assertTrue( kg2 != kg5 )
		self.assertTrue( kg5 != kg2 )
		self.assertFalse( kg2 != kg2b )
		self.assertFalse( kg2b != kg2 )
		
		# Unit > Unit
		self.assertTrue( kg5 > kg2 )
		self.assertFalse( kg2 > kg2b )
		self.assertFalse( kg2 > kg5 )
		
		# Unit >= Unit
		self.assertTrue( kg5 >= kg2 )
		self.assertTrue( kg2 >= kg2b )
		self.assertFalse( kg2 >= kg5 )
		
		# Unit < Unit
		self.assertTrue( kg2 < kg5 )
		self.assertFalse( kg2 < kg2b )
		self.assertFalse( kg5 < kg2 )
		
		# Unit <= Unit
		self.assertTrue( kg2 <= kg5 )
		self.assertTrue( kg2 <= kg2b )
		self.assertFalse( kg5 <= kg2 )
	
	
	def test_comparison_unit_range( self ):
	
		kg2 = unit.Unit.create( "2kg" )
		kg0_1 = unit.Unit.create( "0~1kg" )
		kg1_2 = unit.Unit.create( "1~2kg" )
		kg2_5 = unit.Unit.create( "2~5kg" )
		kg1_6 = unit.Unit.create( "1~6kg" )
		kg5_6 = unit.Unit.create( "5~6kg" )
		
		# Unit == Range
		self.assertTrue( kg2 == kg1_6 )
		self.assertTrue( kg2 == kg1_2 )
		self.assertTrue( kg2 == kg2_5 )
		self.assertFalse( kg2 == kg0_1 )
		self.assertFalse( kg2 == kg5_6 )
		
		# Range == Unit
		self.assertTrue( kg1_6 == kg2 )
		self.assertTrue( kg1_2 == kg2 )
		self.assertTrue( kg2_5 == kg2 )
		self.assertFalse( kg0_1 == kg2 )
		self.assertFalse( kg5_6 == kg2 )
		
		# Unit != Range
		self.assertTrue( kg2 != kg5_6 )
		self.assertTrue( kg2 != kg0_1 )
		self.assertFalse( kg2 != kg1_6 )
		self.assertFalse( kg2 != kg1_2 )
		self.assertFalse( kg2 != kg2_5 )
		
		# Range != Unit
		self.assertTrue( kg5_6 != kg2 )
		self.assertTrue( kg0_1 != kg2 )
		self.assertFalse( kg1_6 != kg2 )
		self.assertFalse( kg1_2 != kg2 )
		self.assertFalse( kg2_5 != kg2 )
		
		# Unit > Range
		self.assertTrue( kg2 > kg0_1 )
		self.assertFalse( kg2 > kg1_6 )
		self.assertFalse( kg2 > kg1_2 )
		self.assertFalse( kg2 > kg2_5 )
		self.assertFalse( kg2 > kg5_6 )
		
		# Unit >= Range
		self.assertTrue( kg2 >= kg0_1 )
		self.assertTrue( kg2 >= kg1_6 )
		self.assertTrue( kg2 >= kg1_2 )
		self.assertTrue( kg2 >= kg2_5 )
		self.assertFalse( kg2 >= kg5_6 )
		
		# Unit < Range
		self.assertTrue( kg2 < kg5_6 )
		self.assertFalse( kg2 < kg2_5 )
		self.assertFalse( kg2 < kg1_2 )
		self.assertFalse( kg2 < kg1_6 )
		self.assertFalse( kg2 < kg0_1 )
		
		# Range < Unit
		self.assertTrue( kg0_1 < kg2 )
		self.assertFalse( kg1_6 < kg2 )
		self.assertFalse( kg1_2 < kg2 )
		self.assertFalse( kg2_5 < kg2 )
		self.assertFalse( kg5_6 < kg2 )
		
		# Unit <= Range
		self.assertTrue( kg2 <= kg5_6 )
		self.assertTrue( kg2 <= kg2_5 )
		self.assertTrue( kg2 <= kg1_2 )
		self.assertTrue( kg2 <= kg1_6 )
		self.assertFalse( kg2 <= kg0_1 )
		
		# Range <= Unit
		self.assertTrue( kg0_1 <= kg2 )
		self.assertTrue( kg1_6 <= kg2 )
		self.assertTrue( kg1_2 <= kg2 )
		self.assertTrue( kg2_5 <= kg2 )
		self.assertFalse( kg5_6 <= kg2 )
		
		
	def test_comparison_range_range( self ):
	
		kg0_1 = unit.Unit.create( "0~1kg" )
		kg0_2 = unit.Unit.create( "0~2kg" )
		kg0_5 = unit.Unit.create( "0~5kg" )
		kg1_3 = unit.Unit.create( "1~3kg" )
		kg2_4 = unit.Unit.create( "2~4kg" )
		
		# Range == Range
		self.assertTrue( kg0_2 == kg1_3 )
		self.assertTrue( kg1_3 == kg0_2 )
		self.assertTrue( kg0_1 == kg1_3 )
		self.assertTrue( kg1_3 == kg0_1 )
		self.assertTrue( kg1_3 == kg2_4 )
		self.assertTrue( kg2_4 == kg1_3 )
		self.assertTrue( kg1_3 == kg0_5 )
		self.assertTrue( kg0_5 == kg1_3 )
		self.assertFalse( kg0_1 == kg2_4 )
		self.assertFalse( kg2_4 == kg0_1 )
		
		# Range != Range
		self.assertFalse( kg0_2 != kg1_3 )
		self.assertFalse( kg1_3 != kg0_2 )
		self.assertFalse( kg0_1 != kg1_3 )
		self.assertFalse( kg1_3 != kg0_1 )
		self.assertFalse( kg1_3 != kg2_4 )
		self.assertFalse( kg2_4 != kg1_3 )
		self.assertFalse( kg1_3 != kg0_5 )
		self.assertFalse( kg0_5 != kg1_3 )
		self.assertTrue( kg0_1 != kg2_4 )
		self.assertTrue( kg2_4 != kg0_1 )
		
		# Range > Range
		self.assertTrue( kg2_4 > kg0_1 )
		self.assertFalse( kg2_4 > kg0_2 )
		self.assertFalse( kg2_4 > kg1_3 )
		self.assertFalse( kg0_1 > kg2_4 )
		self.assertFalse( kg1_3 > kg0_5 )
		self.assertFalse( kg0_5 > kg1_3 )
		
		# Range >= Range
		self.assertTrue( kg2_4 >= kg0_1 )
		self.assertTrue( kg2_4 >= kg0_2 )
		self.assertTrue( kg2_4 >= kg1_3 )
		self.assertFalse( kg0_1 >= kg2_4 )
		self.assertTrue( kg1_3 >= kg0_5 )
		self.assertTrue( kg0_5 >= kg1_3 )
		
		# Range < Range
		self.assertTrue( kg0_1 < kg2_4 )
		self.assertFalse( kg0_2 < kg2_4 )
		self.assertFalse( kg1_3 < kg2_4 )
		self.assertFalse( kg2_4 < kg0_1 )
		self.assertFalse( kg1_3 < kg0_5 )
		self.assertFalse( kg0_5 < kg1_3 )
		
		# Range <= Range
		self.assertTrue( kg0_1 <= kg2_4 )
		self.assertTrue( kg0_2 <= kg2_4 )
		self.assertTrue( kg1_3 <= kg2_4 )
		self.assertFalse( kg2_4 <= kg0_1 )
		self.assertTrue( kg1_3 <= kg0_5 )
		self.assertTrue( kg0_5 <= kg1_3 )

if __name__ == "__main__":
	unittest.main()
