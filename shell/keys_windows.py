# -*- coding: utf-8 -*-

# Key escape regular expression
# While this expression matches, the key sequence is incomplete
escape_regex = b'^(\xe0)?$'

# Registered keys
ENTER = b'\n'
ESCAPE = b'\x1b'
TABULATION = b'\t'
HOME = b'\xe0G'
END = b'\xe0O'
LEFT = b'\xe0K'
CTRL_LEFT = b'\xe0s'
RIGHT = b'\xe0M'
CTRL_RIGHT = b'\xe0t'
UP = b'\xe0H'
DOWN = b'\xe0P'
BACKSPACE = b'\x08'
DELETE = b'\xe0S'
