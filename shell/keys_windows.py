# -*- coding: utf-8 -*-

# Key escape regular expression
# While this expression matches, the key sequence is incomplete
escape_regex = b'^(\xe0)?$'

# Registered keys
ENTER = '\n'
ESCAPE = '\x1b'
TABULATION = '\t'
HOME = '\xe0G'
END = '\xe0O'
LEFT = '\xe0K'
CTRL_LEFT = '\xe0s'
RIGHT = '\xe0M'
CTRL_RIGHT = '\xe0t'
UP = '\xe0H'
DOWN = '\xe0P'
BACKSPACE = '\x08'
DELETE = '\xe0S'
