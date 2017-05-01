# -*- coding: utf-8 -*-

# Key escape regular expression
# While this expression matches, the key sequence is incomplete
escape_regex = b'^(\xe0|\xc2|\xc3)?$'

# Registered keys
ENTER = b'\n'
UNICODE1 = b'\xc2\x00'
UNICODE2 = b'\xc3\x00'
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
