from pysolr import Solr
import requests

class SolrArm(object):
    def __init__(self, armSettings):
        self.grabOptions = armSettings.grabOptions
        self.armOptions = armSettings.arm
        self.returnOptions = armSettings.returnOptions
        self.solrArm = self.newArm()

    def newArm(self):
        arm = self.armOptions
        session = requests.Session()
        if arm['isProtected']:
            session.auth = (arm['username'], arm['password'])
        return Solr(arm['serverUrl'], make_request=session)

    def newGrab(self):
        grab = self.grabOptions
        if grab['pinPoint']:
            return self.solrArm.search(grab['guildLines'])
        if grab['freeThrow']:
            return self.solrArm.search_cursor(**grab['guildLines'])
        if grab['multiHand']:
            return self.solrArm.async_search(grab['guildLines'])

    def newReturn(self):
        place = self.returnOptions
        try:
            self.solrArm.update(place['where'], place['method'], commit=False)
            self.solrArm.commit()
        except Exception as e:
            return e
