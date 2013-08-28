import logging
from AccessControl import ClassSecurityInfo

logger = logging.getLogger("pas.plugins.wikid.auth")


class AuthPlugin(object):
    """ Implements IAuthenticationPlugin
    """
    meta_type = 'WiKID Auth Plugin'
    security = ClassSecurityInfo()

    security.declarePrivate('authenticateCredentials')

    def authenticateCredentials(self, credentials):

        """ See IAuthenticationPlugin.

        o We expect the credentials to be those returned by
          ILoginPasswordExtractionPlugin.
        """
        login = credentials.get('login')
        password = credentials.get('password')

        if login is None or password is None:
            return None
        # check credentials using a wikid server
        connector = self._getWikidConnection()
        res = connector.login(login, password, self.domaincode)
        if res is True:
            return login, login
        else:
            print None
