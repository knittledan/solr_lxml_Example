# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# server.py
#------------------------------------------------------------------------------

import sys
import os

rootPath = os.path.dirname(__file__).split('/server')[0]
serverPath = '/'.join([rootPath, "/server"])
thirdParty = '/'.join([rootPath, "/thirdParty"])
sys.path.insert(0, serverPath)
sys.path.insert(0, thirdParty)

import controller.yml.yamlUtilities as ymlUtils

class ServerConfig(object):
    def __init__(self):
        self.setSourcePaths()

    # set system paths
    def setSourcePaths(self):
        params = ymlUtils.YamlUtilities()
        params.load("core.sourcePaths")
        for k, v in params.parameters.items():
            if k == "sourcePaths":
                for k2, v2 in v.items():
                    sys.path.insert(0, v2)
                    setattr(self, k2, v2)
            else:
                setattr(self, k, v)