# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# yamlUtilities.py
# ------------------------------------------------------------------------------

import os
import re
import gc
import model

from functools import reduce
from yaml import load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

#-------------------------------------------------------------------------------
# object
#-------------------------------------------------------------------------------


class YamlUtilities(object):
    regEx = re.compile("\[(\w*)\]")
    ext = '.yml'

    def __init__(self):
        self.ymlObject = {}
        self.rawParameters = {}
        self.parameters = {}
        self.key = ''

    def __getattr__(self, key):
        print ('YamlUtilities has no attribute %s' % key)

    #---------------------------------------------------------------------------
    def reset(self):
        self.parameters = dict(self.rawParameters)

    def load(self, fileKey):
        fileLoader = model.Model()
        if isinstance(fileKey, list):
            for key in fileKey:
                print(key)
                self.loadProperties(fileLoader.get(key))
        else:
            self.loadProperties(fileLoader.get(fileKey))

    def loadProperties(self, path, filename=None):
        if not filename and os.path.isfile(path):
            yamlFile = path
        else:
            yamlPath = '/'.join([path, filename])
            yamlFile = ''.join([yamlPath, self.ext])
        if os.path.isfile(yamlFile):
            with open(yamlFile, "r") as yFile:
                self.rawParameters.update(load(yFile, Loader=Loader))
            self.parameters.update(self._constructParameters(self.rawParameters).copy())
            gc.collect()

    def getItem(self, key, kDict=None):
        """
        Finds parameter with only one key. Will travers nested dictionary
        until key is found.
        :param key: key1
        :param kDict: is a dictionary
        :return: str or dict
        """
        kDict = kDict or self.parameters
        if isinstance(key, str) and key in kDict:
            return kDict[key]
        if isinstance(key, list) and key[0] in kDict:
            return kDict
        for k, v in kDict.items():
            if isinstance(v, dict):
                item = self.getItem(key, v)
                if item is not None:
                    return item

    def updateItem(self, key, value):
        """
        Updates parameter with only one key. Will travers nested dictionary
        until key is found.
        :param key: key
        :param value: any obj
        :return: None
        """
        self.getItem([key], self.rawParameters)[key] = value
        self.parameters = self._constructParameters(self.rawParameters).copy()
        gc.collect()

    def get(self, key, kDict=None):
        """
        Finds parameter with direct key path key1.subKey2.subKey2
        :param key: key1.subKey2.subKey2
        :param kDict: is a dictionary
        :return: str or dict
        """
        params = kDict or self.parameters
        if not isinstance(key, list):
            if "." in key:
                key = key.split('.')
            else:
                key = [key]
        return reduce(lambda d, k: d[k], key, params)

    def update(self, key, value):
        """
        Updates parameter with direct key path key1.subKey2.subKey2
        :param key: key1.subKey2.subKey2
        :param value: any obj
        :return: None
        """
        if "." in key:
            key = key.split('.')
        else:
            key = [key]
        self.get(key[:-1], self.rawParameters)[key[-1]] = value
        self.parameters = self._constructParameters(
            self.rawParameters).copy()
        gc.collect()

    #---------------------------------------------------------------------------
    # Helpers
    #---------------------------------------------------------------------------

    def _constructParameters(self, d):
        new = {}
        if isinstance(d, dict):
            for k, val in d.items():
                val = self.__constructConditional(val)
                new[k] = self._replaceBrackets(val)
        if isinstance(d, list):
            for idx, val in enumerate(d):
                val    = self.__constructConditional(val)
                d[idx] = self._replaceBrackets(val)
            return d
        return new

    def __constructConditional(self, val):
        return self._constructParameters(val) if type(val) in [dict, list] else val

    def _replaceBrackets(self, string):
        """
        Resolves property variable within a string into a string
        :param string:
        :return:
        """
        m = re.findall(self.regEx, str(string))
        if m:
            for key in m:
                value = self.getItem(key, self.rawParameters)
                if re.findall(self.regEx, str(value)):
                    value = self._replaceBrackets(value)
                string = string.replace('[' + key + ']', value)
            re.purge()
        gc.collect()
        return string