import logging
from AccessControl import ClassSecurityInfo

logger = logging.getLogger("pas.plugins.wikid.useradder")


class UserAdderPlugin(object):
    """ Implements IUserAdderPlugin
    """
    security = ClassSecurityInfo()

    security.declarePrivate('doAddUser')

    def doAddUser(self, login, password):
        logger.debug('calling doAddUser()...')
        connector = self._getWikidConnection()
        # TODO check if exists
        return connector.registerUsername(login, password,
                                          self.domaincode)
