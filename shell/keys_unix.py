# -*- coding: utf-8 -*-

# Key escape regular expression
# While this expression matches, the key sequence is incomplete
escape_regex = b'^(\x1b(\[(1(\;(5)?)?|3)?)?)?$'

# Registered keys
ENTER = b'\n'
ESCAPE = b'\x1b'
TABULATION = b'\t'
HOME = b'\x1b[H'
END = b'\x1b[F'
LEFT = b'\x1b[D'
CTRL_LEFT = b'\x1b[1;5D'
RIGHT = b'\x1b[C'
CTRL_RIGHT = b'\x1b[1;5C'
UP = b'\x1b[A'
DOWN = b'\x1b[B'
BACKSPACE = b'\x7f'
DELETE = b'\x1b[3~'
