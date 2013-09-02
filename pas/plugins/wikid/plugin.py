"""WiKIDAuthPlugin
Copyright(C), 2008, WiKID Systems, Inc - ALL RIGHTS RESERVED

This software is licensed under the Terms and Conditions contained within the
LICENSE.txt file that accompanied this software.  Any inquiries concerning the
scope or enforceability of the license should be addressed to:

WiKID Systems, Inc.
1350 Spring St.
Suite 300
Atlanta, Ga 30309
info at wikidsystems.com
866-244-1876
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from pas.plugins.wikid.client import WikidClient
from pas.plugins.wikid.plugins.auth import AuthPlugin
from pas.plugins.wikid.plugins.base import WiKIDBasePlugin
from pas.plugins.wikid.plugins.enumeration import UserEnumerator


class WiKIDAuthMultiPlugin(WiKIDBasePlugin, AuthPlugin, UserEnumerator):

    """ PAS plugin for using WiKID credentials to log in.
    """

    meta_type = 'WiKID Auth Multi Plugin'

    security = ClassSecurityInfo()
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


InitializeClass(WiKIDAuthMultiPlugin)
