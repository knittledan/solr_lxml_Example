solr_lxml_Example
=================

python code demonstrating solr and lxml

Supported: Mac osx. Python2.7 & python3.2

lxml and yaml are compiled only for and Python2.7 & python3.2

Example executable code is found in:
/solr_lxml_Example/server/core

When any app starts a yaml file is read in and adds defined system paths to sys.paths. Paths are defined under:
/solr_lxml_Example/server/model/core/sourcePaths.yml

solrSearch.py:
--------------
Loads parameters from a yaml file. properties file is loaded from: /solr_lxml_Example/server/model/solr/properties/solrServerProperties.yml

Once loaded a new server is started in a new thread that binds to 127.0.0.1:8983. 
Then a query is performs with the given user text. 
User text is sanitized and check for a minimum length of 3 characters long before passing into solr server search. 
Results are printed out in the form of a list of dictionaries. 

xmlEditing.py:
--------------
A new solr core is created and placed under /solr_lxml_Example/cores/. The name and atrributes for the new core are added into solr.xml. Once the new core is created you can start the solr server and view the new core in http://127.0.0.1:8983/solr

xmlEditing() loads the solrTest.xml and shows the tools and interface avaliable for manipulating xml files. 

yamlUtilities:
--------------
Yaml utilities loads a yaml file then updates any value by replacing all [] brackets with the value of the corrisponding key. This allows the reuse and manipulation of parameters. Values can be nested lists, dictionaries, or strings.

