from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin

from pas.plugins.wikid.client import WikidClient


class WiKIDBasePlugin(BasePlugin):
    """ It's a mixin for WiKIDAuthMultiPlugin
    """
    meta_type = 'WiKIDBasePlugin'
    security = ClassSecurityInfo()

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title
        self.wikid_port = 8388
        self.wikid_host = "127.0.0.1"
        self.domaincode = '127000000001'
        self.passPhrase = 'passphrase'
        self.caCert = ''
        self.pkey = ''

    security.declarePrivate('_getWikidConnection')

    def _getWikidConnection(self):
        # '_v_connector' will not be persisted due to '_v_'
        if not hasattr(self, '_v_connector'):
            self._v_connector = WikidClient(
                host=self.wikid_host,
                port=self.wikid_port,
                pkey=self.pkey,
                pass_phrase=self.passPhrase,
                cacert=self.caCert
            )
            self._v_connector.setUpConnection()
        return self._v_connector

InitializeClass(WiKIDBasePlugin)
