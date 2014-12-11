
import subprocess
import controller.yml.yamlUtilities as ymlUtils
from threading import Thread

class SolrServer(Thread):
    params = ymlUtils.YamlUtilities()
    params.load(["core.sourcePaths", "solr.properties.solrServerProperties"])

    def __init__(self):
        try:
            super().__init__(name=self.params.get("title"))
        except TypeError:
            Thread.__init__(self, name=self.params.get("title"))

    def run(self):
        print(self.params.get("startCmd"))
        subprocess.call(self.params.get("startCmd"))

#  update command
# java -Durl=http://localhost:8983/solr/usaStates/update  -Dsolr.solr.home=/home/codingcobra/Desktop/tailswitch/cores -Djetty.home=/home/codingcobra/Desktop/tailswitch/thirdParty/solr -Djetty.port=8983 -jar /home/codingcobra/Desktop/tailswitch/thirdParty/solr/exampledocs/post.jar /home/codingcobra/Downloads/tailswitchExport/plainScheme/states.xml