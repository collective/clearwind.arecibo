from zope.component import adapts

from Products.GenericSetup.interfaces import ISetupEnviron
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import I18NURI
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import NodeAdapterBase
from Products.GenericSetup.utils import ObjectManagerHelpers
from Products.GenericSetup.utils import PropertyManagerHelpers
from Products.GenericSetup.utils import XMLAdapterBase
from Products.CMFCore.utils import getToolByName
from interfaces import IAreciboConfiguration
    

class AreciboXMLAdapter(XMLAdapterBase, ObjectManagerHelpers):
    """
    XML importer and exporter for Arecibo.
    """
    adapts(IAreciboConfiguration, ISetupEnviron)
    _LOGGER_ID = 'clearwind.arecibo'
    name = 'arecibo'
    
    def _extractSettings(self):
        fragment = self._doc.createDocumentFragment()
        for setting in ['account_number', 'app_name', 'transport', 'ignore_localhost']:
            child = self._doc.createElement(setting)
            child.appendChild(self._doc.createTextNode(str(self.context.__getattribute__(setting))))
            fragment.appendChild(child)

        return fragment
    
    def _exportNode(self):
        node = self._getObjectNode('object')
        node.setAttribute('name', 'arecibo')
        node.setAttribute('meta_type', 'configuration')
        node.appendChild(self._extractSettings())
        self._logger.info('Arecibo exported.')
        return node

    
    def _initSettings(self, node):
        config = self.context.getSiteManager().queryUtility(IAreciboConfiguration, name='Arecibo_config')
        
        for child in node.childNodes:
            if not child.childNodes or not len(child.childNodes):
                continue
            if child.nodeName == 'ignore_localhost':
                if child.childNodes[0].data == 'True':
                    config.__setattr__(child.nodeName, True)
                else:
                    config.__setattr__(child.nodeName, False)
            else:
                config.__setattr__(child.nodeName, child.childNodes[0].data)

    
    def _importNode(self, node):
        if self.environ.shouldPurge():
            self._purgeObjects()

        self._initSettings(node)
        self._logger.info('Arecibo settings imported.')
        
        
def importAreciboSettings(context):
    qu = context.getSite().getSiteManager().queryUtility(IAreciboConfiguration, name='Arecibo_config')
    if qu: # XXX: not really sure if things ever actually get in here...
        importObjects(qu, '', context)


def exportAreciboSettings(context):
    qu = context.getSite().getSiteManager().queryUtility(IAreciboConfiguration, name='Arecibo_config')
    exportObjects(qu, '', context) 
    
    
