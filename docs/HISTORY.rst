Changelog
=========

0.7 (unreleased)
----------------
 - Update getSite location for Plone 4.3 compatibility. [esteele]

0.6 (2011-09-22)
----------------
 - HTTP Post to throw-away threads [supton]
 - remove incompatible 4.1 import [supton]

0.5 (2011-06-20)
----------------
 - Merge HISTORY.txt's [eleddy]
 - Add z3c.autoinclude to so that zcml slugs are not needed [eleddy]
 - Get smtp_from from portal properties [eleddy]
 - Add app_name to configuration panel so that the urls for posting 
   and email can be automatically generated [eleddy]
 - Fix control panel icon [eleddy]
 - GenerisSetup export/import [eleddy]
 - Add configuration to ignore localhost errors [eleddy]
 - Ignore errors based on the plone configuration of ignored errors [eleddy]
 

0.2 > 0.3:
----------
- Removed the skins and layers

- Made it catch all errors (even Zope ones) by patching SiteErrorLog

- Allowed the override of configuration values by the use of site_configuration.py

- Added in the ignores property

- Made uninstalling remove configlet

- Made install optional (just site_configuration.py will be enough)

- Any errors sending to Arecibo are logged
