# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# solrXML.py
#------------------------------------------------------------------------------

import lxml
from lxml import etree as ET

def elementArg(func):
    def wrapper(*args):
        etType  = lxml.etree._Element
        cls     = args[0]
        element = args[1]
        if isinstance(element, etType):
            element = element
        else:
            element = cls.selectElement(element)
        if isinstance(element, etType):
            func(cls, element, *args[2:])
        else:
            raise Exception("Unable to find xml element: %(element)s" % locals())
    return wrapper

# TODO: add delete attribute, delete element
class SolrXML(object):
    def __init__(self, filePath):
        self.xmlFile = filePath
        self.tree    = ET.parse(filePath)

    @elementArg
    def updateText(self, element, value):
        '''
        <elementPointer>value</elementPointer>
        :param elementPointer: tree path to element.
        :param value: the new value
        :return:
        '''
        if len(element.text.replace('\n', '').strip()) > 0:
            element.text = value

    @elementArg
    def addAttr(self, element, attribute, value):
        element.attrib[attribute] = value

    @elementArg
    def updateAttr(self, element, attribute, value):
        '''
        <element attribute="value">id</element>
        :param attribute: name of attribute to be updated
        :param value: the new value
        :param element: already selected xml element
        :return:
        '''
        if element.attrib.get(attribute):
            element.attrib.update({attribute : value})
        else:
            raise Exception("Unable to find %(element)s attribute: %(attribute)s" % locals())

    def addElement(self, container, elementTag, **kwargs):
        attributes   = kwargs['attributes']
        container    = self.selectElement(container)
        if not self.elementExists(container, elementTag, **attributes):
            newCore = ET.Element("core", **attributes)
            newCore.tail = "\n\n"
            container.insert(-1, newCore)

    def removeElement(self, elementPointer, **kwargs):
        attributes = kwargs['attributes']
        element    = self.selectElement(elementPointer, **attributes)
        if element:
            element.getparent().remove(element)

    def selectElement(self, elementPointer, **attributes):
        if elementPointer is None:
            return self.root

        elementTree = elementPointer.split(".")
        elementTag  = elementTree[-1]

        if attributes:
            signiture   = "[@%s='%s']"
            signiture   = ''.join([signiture % (k,v) for k, v in attributes.items()])
            finalLayout = "//%(elementTag)s%(signiture)s" % locals()
            elements    = self.root.xpath(finalLayout)[0]
            return elements[0] if elements else None

        element = self.root
        for x in elementTree:
            element = element[0].xpath('//%(x)s' % locals())
        # elements = self.root.xpath('//%(elementTag)s' % locals())
        return element[0] if element else None

    def save(self):
        self.tree.write(self.xmlFile,
                   pretty_print=True,
                   xml_declaration=True,
                   encoding='ASCII')

    def printTree(self, element):
        element = element if element else self.root
        print(ET.tostring(element, pretty_print=True, encoding='ASCII', xml_declaration=True))

    @staticmethod
    def elementExists(element, elementTag, **attributes):
        """//core[@name='%s']"""
        signiture   = "[@%s='%s']"
        signiture   = ''.join([signiture % (k,v) for k, v in attributes.items()])
        finalLayout = "//%(elementTag)s%(signiture)s" % locals()
        return len(element.xpath(finalLayout)) > 0

    @property
    def root(self):
        return self.tree.getroot()