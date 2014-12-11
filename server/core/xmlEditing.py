#! /usr/bin/env python
#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# tailswitch
#------------------------------------------------------------------------------
import time
from config.serverConfig import ServerConfig
server = ServerConfig()

import controller.solr.createCore as createCore
import controller.yml.yamlUtilities as yUtils
import controller.yml.yamlUtilities as yUtils

from controller.solr.solrServer import SolrServer
from controller.xml import solrXML

#------------------------------------------------------------------------------
# exposed methods
#------------------------------------------------------------------------------

def newCore():
    """
    Creates a new solr core. Adds core name into solr.xml.
    New core is avaliable in solr webapp. Start the solr server.
    """
    coreName       = "testCore2"
    coreProperties = "solr.properties.coreProperties"

    options = yUtils.YamlUtilities()
    options.load(coreProperties)
    test = createCore.CreateCore(options)
    test.createCore(coreName)

newCore()

def startSolrServer():
    """
    Starts the solr server in a new thread.
     server url http://127.0.0.1:8983/solr
    """
    test = SolrServer()
    test.start()
    time.sleep(4)


def xmlEditing():
    """
    Loads an xml file.
    Adds attributes into tree. Updates attributes. Remove elements.
    """
    coreProperties  = "solr.properties.coreProperties"
    solrFilePathKey = "solrTestProperties"

    options = yUtils.YamlUtilities()
    options.load(coreProperties)
    solrFile = options.get(solrFilePathKey)
    solrClass = solrXML.SolrXML(solrFile)

    # example code

    print("Example file: ", solrFile)
    # select element shardHandlerFactory.str
    element = solrClass.selectElement("shardHandlerFactory.str")
    # print its info
    print(element.tag, element.attrib, element.text)
    # update its info
    solrClass.addAttr("shardHandlerFactory.str", "person", "dan")
    # print its info
    print(element.tag, element.attrib, element.text)
    # create new element
    solrClass.addElement("solr.shardHandlerFactory", "demoElement",
                         attributes={"test": "asdfsad"})
    element = solrClass.selectElement("shardHandlerFactory.demoElement")
    # print its info
    print(element.tag, element.attrib)
    # save the file
    solrClass.save()

# xmlEditing()