import logging
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.PluggableAuthService.interfaces.plugins import IUserAdderPlugin

logger = logging.getLogger("pas.plugins.wikid.useradder")


class UserAdderPlugin(object):
    """ Implements IUserAdderPlugin
    """
    implements(IUserAdderPlugin)
    security = ClassSecurityInfo()

    security.declarePrivate('doAddUser')

    def doAddUser(self, login, regcode):
        logger.debug('calling doAddUser()...')
        connector = self._getWikidConnection()
        return connector.registerUsername(login, regcode,
                                          self.domaincode)
