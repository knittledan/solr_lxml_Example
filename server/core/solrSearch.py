#! /usr/bin/env python
#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# tailswitch
#------------------------------------------------------------------------------
from config.serverConfig import ServerConfig
import time
server = ServerConfig()
#------------------------------------------------------------------------------
# exposed methods
#------------------------------------------------------------------------------

def startSolrServer():
    from controller.solr.solrServer import SolrServer
    test = SolrServer()
    test.start()
    time.sleep(4)
    # from controller.solr import indexRequest
    # indexRequest.IndexRequest()
startSolrServer()

def locationSerach():
    from controller.solr.search.locationLookup import LocationLookup
    test = LocationLookup("localhost", 8983, "locationData")


    # example code

    test.search("mount washington")
    results1 = test.results.documents
    test.search("89506 ren")
    results2 = test.results.documents
    test.search("monica")
    results3 = test.results.documents
    test.search("90016")
    results4 = test.results.documents
    print('\n-------------------\n')
    print("mount washington : ", results1)
    print("89506 ren:       : ", results2)
    print("monica           : ", results3)
    print("90016            : ", results4)
locationSerach()
