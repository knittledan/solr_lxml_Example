#! /usr/bin/env python
#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# tailswitch
#------------------------------------------------------------------------------
from config.serverConfig import ServerConfig
server = ServerConfig()
#------------------------------------------------------------------------------
# exposed methods
#------------------------------------------------------------------------------

class NewCore(ServerConfig):
    def __init__(self):
        ServerConfig.__init__(self)
        import controller.solr.createCore as createCore
        import controller.yml.yamlUtilities as yUtils
        options = yUtils.YamlUtilities()
        options.load("solr.properties.coreProperties")
        test = createCore.CreateCore(options)
        test.createCore("testCore2")
NewCore()


def xmlEditing():
    from controller.xml import solrXML
    import controller.yml.yamlUtilities as yUtils
    options = yUtils.YamlUtilities()
    options.load("solr.properties.coreProperties")
    solrFile = options.get("solrTestProperties")
    solrClass = solrXML.SolrXML(solrFile)

    # example code

    print(solrFile)
    element = solrClass.selectElement("shardHandlerFactory.str")
    solrClass.updateText("solr", "sadfasdfasd")
    print(element.tag, element.text)
    solrClass.addAttr("shardHandlerFactory.str", "person", "dan")
    print(element.tag, element.attrib, element.text)
    solrClass.updateAttr("shardHandlerFactory.str", "person", "violet")
    print(element.tag, element.attrib, element.text)
    solrClass.save()

xmlEditing()