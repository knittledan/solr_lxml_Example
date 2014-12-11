# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# __init__.py
#------------------------------------------------------------------------------

import os

modelPath = os.path.normpath(os.path.dirname(__file__))


class Model(object):
    def __init__(self):
        self.files = {}
        for root, dirs, files in os.walk(modelPath):
            depth = root[len(modelPath) + len(os.path.sep):].count(os.path.sep) + 1
            for momo in files:
                if momo[:1].isalpha():
                    keyPath = root.rsplit('/', depth)[1:]
                    refName = momo.split('.')[0]
                    keyPath.append(refName)
                    key = '.'.join(keyPath)
                    self.files[key] = '/'.join([root, momo])

    def get(self, key):
        return self.files[key]