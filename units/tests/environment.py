# -*- coding: utf-8 -*-

import os
import sys

basepath = os.path.dirname( os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ) )

sys.path.append( basepath )
os.chdir( basepath )

from language import Language
Language.initialize( lang="en", path=basepath + os.sep + "i18n" )

