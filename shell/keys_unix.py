# -*- coding: utf-8 -*-

# Key escape regular expression
# While this expression matches, the key sequence is incomplete
escape_regex = b'^(\x1b(\[(3|1(\;(5)?)?)?)?)?$'

# Registered keys
ENTER = '\n'
ESCAPE = '\x1b'
TABULATION = '\t'
HOME = '\x1b[H'
END = '\x1b[F'
LEFT = '\x1b[D'
CTRL_LEFT = '\x1b[1;5D'
RIGHT = '\x1b[C'
CTRL_RIGHT = '\x1b[1;5C'
UP = '\x1b[A'
DOWN = '\x1b[B'
BACKSPACE = '\x7f'
DELETE = '\x1b[3~'
