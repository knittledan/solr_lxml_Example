
import subprocess
import osUtilities
import controller.yml.yamlUtilities as ymlUtils

from threading import Thread

class SolrServer(Thread):
    """
    Solr Server Commands. Load parameters from model.solr.properties package.
    """
    params = ymlUtils.YamlUtilities()
    params.load(["core.sourcePaths", "solr.properties.solrServerProperties"])

    def __init__(self):
        """
        Initialize super depending on python version
        """
        if osUtilities.isPy32():
            super().__init__(name=self.params.get("title"))
        else:
            Thread.__init__(self, name=self.params.get("title"))

    def run(self):
        """
        starts the solr server
        """
        subprocess.call(self.params.get("startCmd"))