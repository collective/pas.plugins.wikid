import os
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from AccessControl.requestmethod import postonly

from Products.CMFCore.permissions import ManagePortal
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin

from pas.plugins.wikid.client import WikidClient


class WiKIDBasePlugin(BasePlugin):

    meta_type = 'WiKIDBasePlugin'
    security = ClassSecurityInfo()

    security.declarePrivate('_getWikidConnection')

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title
        self.wikid_port = 8388
        self.wikid_host = "127.0.0.1"
        self.domaincode = '127000000001'
        self.passPhrase = 'passphrase'
        self.caCert = ''
        self.pkey = ''

    def _getWikidConnection(self):
        # '_v_connector' will not be persisted due to '_v_'
        if not hasattr(self, '_v_connector'):
            try:
                self._v_connector = WikidClient(
                    host=self.wikid_host,
                    port=self.wikid_port,
                    pkey=self.pkey,
                    pass_phrase=self.passPhrase,
                    cacert=self.caCert
                )
                self._v_connector.setUpConnection()
            except:
                return None
        return self._v_connector

InitializeClass(WiKIDBasePlugin)
