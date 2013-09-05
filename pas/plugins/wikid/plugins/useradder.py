import logging
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.PluggableAuthService.interfaces.plugins import IUserAdderPlugin
from Products.PluggableAuthService.utils import createViewName

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
        success = connector.registerUsername(login, regcode, self.domaincode)
        if success:
            # Invalidate the cache
            view_name = createViewName('enumerateUsers')
            self.ZCacheable_invalidate(view_name=view_name)
        return success
