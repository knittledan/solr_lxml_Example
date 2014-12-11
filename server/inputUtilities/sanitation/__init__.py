# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# __init__.py
#------------------------------------------------------------------------------

import re

_reAlpha        = re.compile(r'[^a-zA ]')
_reNumeric      = re.compile(r'[^0-9 ]')
_reAlphaNumeric = re.compile(r'[^a-zA-Z0-9 ]')
_reBasicText    = re.compile(r'[^a-zA-Z0-9 \-_\',"]')

def textAlphaNumeric(f):
    def wrapper(*args):
        cls       = args[0]
        userInput = args[1]
        userInput = _reAlphaNumeric.sub("", userInput)
        f(cls, userInput)
    return wrapper

def textAlpha(f):
    def wrapper(*args):
        cls       = args[0]
        userInput = args[1]
        userInput = _reAlpha.sub("", userInput)
        f(cls, userInput)
    return wrapper

def textNumeric(f):
    def wrapper(*args):
        cls       = args[0]
        userInput = args[1]
        userInput = _reNumeric.sub("", userInput)
        f(cls, userInput)
    return wrapper

def textBasicText(f):
    def wrapper(*args):
        cls       = args[0]
        userInput = args[1]
        userInput = _reBasicText.sub("", userInput)
        f(cls, userInput)
    return wrapper