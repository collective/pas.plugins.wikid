import os

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from AccessControl.requestmethod import postonly
from Products.CMFCore.permissions import ManagePortal
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin

from pas.plugins.wikid.client import WikidClient


class WiKIDBasePlugin(BasePlugin):
    """ It's a mixin for WiKIDAuthMultiPlugin
    """
    meta_type = 'WiKIDBasePlugin'

    security = ClassSecurityInfo()

    # ZMI tab for configuration page
    manage_options = (({'label': 'Configuration',
                        'action': 'manage_config'},)
                      + BasePlugin.manage_options)

    security.declareProtected(ManagePortal, 'manage_config')
    manage_config = PageTemplateFile('../www/config', globals(),
                                     __name__='manage_config')

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title
        self.wikid_port = 8388
        self.wikid_host = "127.0.0.1"
        self.domaincode = '127000000001'
        self.passPhrase = 'passphrase'
        self.caCert = ''
        self.pkey = ''

    security.declareProtected(ManagePortal, 'manage_updateConfig')

    @postonly
    def manage_updateConfig(self, REQUEST):
        """Update configuration of Trusted Proxy Authentication Plugin.
        """
        def verify():
            msg = "Configuration Error: "

            try:
                int(wikid_port)
            except ValueError:
                return msg + "  'Port' must be an integer."
            if not os.path.exists(pkey):
                return msg + " Cannot access to '%s' No such file." % pkey
            if not os.path.exists(caCert):
                return msg + " Cannot access to '%s' No such file." % caCert
            try:
                WikidClient(host=wikid_host, port=wikid_port, pkey=pkey,
                            pass_phrase=passPhrase, cacert=caCert)
            except:
                return msg + " WIKID Client error. Check certificates."

        response = REQUEST.response
        wikid_port = REQUEST.form.get('wikid_port')
        wikid_host = REQUEST.form.get('wikid_host')
        domaincode = REQUEST.form.get('domaincode')
        passPhrase = REQUEST.form.get('passPhrase')
        caCert = REQUEST.form.get('caCert')
        pkey = REQUEST.form.get('pkey')

        err = verify()
        if not err:
            self.wikid_port = int(wikid_port)
            self.wikid_host = wikid_host
            self.domaincode = domaincode
            self.passPhrase = passPhrase
            self.caCert = caCert
            self.pkey = pkey

            response.redirect('%s/manage_config?manage_tabs_message=%s' %
                              (self.absolute_url(), 'Configuration+updated.'))
        else:
            response.redirect('%s/manage_config?manage_tabs_message=%s' %
                              (self.absolute_url(),
                               err + ' Configuration+NOT+updated.'))

InitializeClass(WiKIDBasePlugin)
