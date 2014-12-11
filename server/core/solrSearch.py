#! /usr/bin/env python
#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# tailswitch
#------------------------------------------------------------------------------
from config.serverConfig import ServerConfig
from controller.solr.solrServer import SolrServer
from controller.solr.search.locationLookup import LocationLookup

import time
server = ServerConfig()

#------------------------------------------------------------------------------
# exposed methods
#------------------------------------------------------------------------------

def startSolrServer():
    """
    Starts the solr server in a new thread.
     server url http://127.0.0.1:8983/solr
    """
    test = SolrServer()
    test.start()
    time.sleep(4)

def locationSerach():
    """
    Search the solr locationData database for a given location.
    format as zipcode, city, or zipcode & city
    """
    startSolrServer()
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
