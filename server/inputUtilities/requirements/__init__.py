# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# __init__.py
#------------------------------------------------------------------------------

def minInputLength(length):
    def decorator(f):
        def wrapper(*args):
            cls       = args[0]
            userInput = args[1]
            if len(userInput) < length:
                return False
            f(cls, userInput)
        return wrapper
    return decorator