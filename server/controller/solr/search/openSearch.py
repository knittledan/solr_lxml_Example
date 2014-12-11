# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# openSearch.py
#------------------------------------------------------------------------------

import requests
import threading
from pysolr import Solr
from controller.solr import isServerOn


class OpenSearch(object):
    def __init__(self, host, port, core):
        assert isinstance(core, str)
        assert isinstance(port, int)
        assert isinstance(host, str)
        self.host = host
        self.port = port
        self.core = core
        self.stream = self.openStream()

    def openStream(self):
        session = requests.Session()
        session.auth = ('admin', 'admin')
        coreUri = 'http://%(host)s:%(port)d/solr/%(core)s' % self.__dict__
        return Solr(coreUri, make_request=session)

    def checkServer(self):
        for threadObj in threading.enumerate():
            print(threadObj.name)