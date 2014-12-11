# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# createCore.py
#------------------------------------------------------------------------------

import os

from distutils import dir_util
from lxml import etree as ET

from inputUtilities import sanitation
from inputUtilities import requirements

try:
    import configparser
except ImportError:
    from backports import configparser


# TODO: Create solr xml utility. Update. Delete. Add values. 
class CreateCore(object):

    DATA_DIR = "${solr.%s.data.dir:}"

    def __init__(self, options):
        self.tree    = None
        self.options = options
        self.coreName = self.options.get("coreName")
        self.configFile = configparser.RawConfigParser()

    @sanitation.textAlphaNumeric
    @requirements.minInputLength(3)
    def createCore(self, coreName):
        self.options.update("coreName", coreName)
        self.coreName = coreName

        templateCore = self.options.get('coreTemplate')
        coreDir      = self.options.get('newCore')
        if not os.path.isdir(coreDir):
            os.makedirs(coreDir)
            if os.path.isdir(templateCore):
                dir_util.copy_tree(templateCore, coreDir)
        self.setCorename()

    def setCorename(self):
        # update new core data dir
        xmlFile = self.options.get('corePropertyPath')
        if os.path.isfile(xmlFile):
            root = self.loadXMLRoot(xmlFile)
            if root.find("dataDir") is not None:
                root.find("dataDir").text = self.DATA_DIR % self.coreName
            updateHandler = root.find("updateHandler")
            if updateHandler is not None:
                updateLog = updateHandler.find("updateLog")
                updateLog.find("str").text = self.DATA_DIR % self.coreName
            self.writeXML(xmlFile)

        xmlFile = self.options.get('schemaPath')
        if os.path.isfile(xmlFile):
            root = self.loadXMLRoot(xmlFile)
            if root.attrib.get("name"):
                root.attrib.update({"name" : self.coreName})
                self.writeXML(xmlFile)


        # set core name and dir inside solr.xml
        xmlFile = self.options.get('solrProperties')
        if os.path.isfile(xmlFile):
            # update the solr properties file with the new core
            root = self.loadXMLRoot(xmlFile)
            cores = root.find("cores")
            if not cores.xpath("//core[@name='%s']" % self.coreName):
                newCore = ET.Element("core",
                                     name=self.coreName,
                                     instanceDir=self.coreName)
                newCore.tail = "\n\n"
                cores.insert(-1, newCore)
                self.writeXML(xmlFile)

    def loadXMLRoot(self, xmlFile):
        self.tree = ET.parse(xmlFile)
        return self.tree.getroot()
        
    def writeXML(self, xmlFile):
        self.tree.write(xmlFile,
                   pretty_print=True,
                   xml_declaration=True,
                   encoding='ASCII')