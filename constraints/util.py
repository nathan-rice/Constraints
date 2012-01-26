"""
util provides some simple wrappers for commonly used built-in functions that
are frequently used in validation.  This module is likely to change in the
future.
"""

import re

def _any(iterable):
    return lambda x = None: any(iterable)

def _all(iterable):
    return lambda x = None: all(iterable)

def _isinstance(class_or_type_or_tuple):
    return lambda x = None: isinstance(x, class_or_type_or_tuple)

def _sum(sequence):
    return lambda x = None: sum(sequence)

def _round(number):
    return lambda x = None: round(number)

def _callable(obj):
    return lambda x = None: callable(x)

def _issubclass(B):
    return lambda x: issubclass(x, B)

def _min(iterable):
    return lambda x = None: min(iterable)

def _max(iterable):
    return lambda x = None: max(iterable)

def matches(other):
    rexpr = re.compile(other)
    return lambda x: rexpr.match(x)
