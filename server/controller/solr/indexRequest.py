# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# indexRequest.py
#------------------------------------------------------------------------------

from pysolr import Solr
import requests

class IndexRequest(object):
    def __init__(self):
        session = requests.Session()
        session.auth = ("admin", "admin")
        solr = Solr("http://localhost:8983/solr/usaStates", make_request=session)
        # solr.update(["/home/codingcobra/Downloads/tailswitchExport/plainScheme/all_zip_codes.xml"], 'xml', commit=False)
        solr.update(["/home/codingcobra/Downloads/tailswitchExport/plainScheme/states.xml"], 'xml', commit=False)

IndexRequest()