from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.component import getUtility

from interfaces import IAreciboConfiguration

from OFS.SimpleItem import SimpleItem

class AreciboConfiguration(SimpleItem):
    implements(IAreciboConfiguration)
    account_number = FieldProperty(IAreciboConfiguration['account_number'])
    app_name = FieldProperty(IAreciboConfiguration['app_name'])
    transport = FieldProperty(IAreciboConfiguration['transport'])
    
def form_adapter(context):
    return getUtility(IAreciboConfiguration, name='Arecibo_config', context=context)