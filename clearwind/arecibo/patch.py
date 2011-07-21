from Products.SiteErrorLog import SiteErrorLog
from zope.app.component.hooks import getSite
from wrapper import arecibo 
import traceback

old_raising = SiteErrorLog.SiteErrorLog.raising
def raising(self, *args, **kw): 
    site = getSite()
    if site and site.meta_type == "Plone Site":
        err = str(getattr(args[0][0], '__name__', args[0][0]))
        tb = "\n".join(traceback.format_tb(args[0][2]))
        msg = args[0][1]
        arecibo(self, error_type=err, error_tb=tb, error_msg=msg)
    return old_raising(self, *args, **kw)
                             
SiteErrorLog.SiteErrorLog.raising = raising
