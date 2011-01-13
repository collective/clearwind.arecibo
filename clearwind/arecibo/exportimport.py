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


class AreciboNodeAdapter(NodeAdapterBase, PropertyManagerHelpers):
    """
    Node importer and exporter for Arecibo
    """

    adapts(IAreciboConfiguration, ISetupEnviron)

    def _exportNode(self):
        node = self._getObjectNode('object')
        node.appendChild(self._extractProperties())
        return node

    def _importNode(self, node):
        purge = self.environ.shouldPurge()
        if node.getAttribute('purge'):
            purge = self._convertToBoolean(node.getAttribute('purge'))
        if purge:
            self._purgeProperties()

        self._initProperties(node)

    node = property(_exportNode, _importNode)
    

class AreciboXMLAdapter(XMLAdapterBase, ObjectManagerHelpers):
    """
    XML importer and exporter for Arecibo.
    """
    adapts(IAreciboConfiguration, ISetupEnviron)
    _LOGGER_ID = 'clearwind.arecibo'
    name = 'arecibo'
    
    def _extractSettings(self):
        fragment = self._doc.createDocumentFragment()
        for setting in ['account_number', 'app_name', 'transport']:
            child = self._doc.createElement(setting)
            child.appendChild(self._doc.createTextNode(self.context.__getattribute__(setting)))
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
        #import pdb; pdb.set_trace()
        for child in node.childNodes:
        
            self.context.__setattr__(node)
            
            provider_id = str(child.getAttribute('name'))
            if child.hasAttribute('remove'):
                if provider_id in self.context.listActionProviders():
                    self.context.deleteActionProvider(provider_id)
                continue

            if provider_id not in self.context.listActionProviders():
                self.context.addActionProvider(provider_id)

    
    def _importNode(self, node):
        if self.environ.shouldPurge():
            self._purgeObjects()

        self._initSettings(node)
        self._logger.info('Arecibo settings imported.')
        
        
def importAreciboSettings(context):
    #import pdb; pdb.set_trace()
    qu = context.getSite().getSiteManager().queryUtility(IAreciboConfiguration, name='Arecibo_config')
    importObjects(qu, '', context)

def exportAreciboSettings(context):
    qu = context.getSite().getSiteManager().queryUtility(IAreciboConfiguration, name='Arecibo_config')
    exportObjects(qu, '', context) 
    
    
