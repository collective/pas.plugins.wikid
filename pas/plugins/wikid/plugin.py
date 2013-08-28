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

import os
from Globals import InitializeClass
from OFS.Cache import Cacheable
from AccessControl import ClassSecurityInfo
from AccessControl.requestmethod import postonly

from Products.CMFCore.permissions import ManagePortal
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin

from pas.plugins.wikid.client import WikidClient
from pas.plugins.wikid.plugins.auth import AuthPlugin
from pas.plugins.wikid.plugins.base import WiKIDBasePlugin


class WiKIDAuthMultiPlugin(WiKIDBasePlugin, AuthPlugin):

    """ PAS plugin for using WiKID credentials to log in.
    """

    meta_type = 'WiKID Auth Multi Plugin'

    security = ClassSecurityInfo()

    # ZMI tab for configuration page
    manage_options = (({'label': 'Configuration',
                        'action': 'manage_config'},)
                      + BasePlugin.manage_options
                      + Cacheable.manage_options)

    security.declareProtected(ManagePortal, 'manage_config')
    manage_config = PageTemplateFile('www/config', globals(),
                                     __name__='manage_config')

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

classImplements(WiKIDAuthMultiPlugin, IAuthenticationPlugin)

InitializeClass(WiKIDAuthMultiPlugin)
