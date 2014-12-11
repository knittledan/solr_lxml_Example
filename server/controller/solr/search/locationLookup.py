# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# locationLookup.py
#------------------------------------------------------------------------------

import re
import controller.yml.yamlUtilities as yUtils
from inputUtilities import sanitation
from inputUtilities import requirements
from .openSearch import OpenSearch
# from controller.tsLogging import TsLoggin

class LocationLookup(OpenSearch):

    _reDigits = re.compile('[^\d]')
    _reAlphas = re.compile('[^a-zA-Z ]')
    params    = yUtils.YamlUtilities()
    params.load("solr.formats.locationSearchFormat")
    returnFields = params.get("returnFields")
    # logger       = TsLoggin("functionTest.log", "TestLogger")

    def __init__(self, host, port, core):
        super(LocationLookup, self).__init__(host, port, core)
        self.results = None
        self.query   = {}
        self.query.update(self.returnFields)

    @sanitation.textAlphaNumeric
    @requirements.minInputLength(3)
    def search(self, userInput):
        self.reset()
        msg = "User Input: %(userInput)s" % locals()
        # self.logger.log(msg, isInfo=True)
        if self.constructQuery(userInput):
            self.results = self.stream.search(**self.query)

    def reset(self):
        self.params.load("solr.formats.locationSearchFormat")
        self.returnFields = self.params.get("returnFields")

    def constructQuery(self, userInput):
        merges = []

        if any(filter(str.isdigit, userInput)):
            zipCode = self._reDigits.sub(r"", userInput)
            q       = self.params.get("zipQuery")['q'] % int(zipCode.strip())
            merges.append(q)

        if any(filter(str.isalpha, userInput)):
            text = self._reAlphas.sub(r"", userInput).strip()
            if ' ' in text:
                text = '"%s"' % text
            q    = self.params.get("cityQuery")['q'] % text
            merges.append(q)

        if merges:
            self.params.get("query")['q'] %= ' AND '.join(merges)
            self.query.update(self.params.get("query"))
            return True

        raise Exception("Search query could not be constructed: \n %(merges)s" % locals())

