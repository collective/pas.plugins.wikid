from AccessControl import ClassSecurityInfo
from zope.interface import implements
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin, IExtractionPlugin


class AuthPlugin(object):
    """ It's a mixin for WiKIDAuthMultiPlugin
    """
    implements(IAuthenticationPlugin, IExtractionPlugin)
    meta_type = 'WiKID Auth Plugin'
    security = ClassSecurityInfo()

    security.declarePrivate('extractCredentials')

    def extractCredentials(self, request):
        if '__ac_name' in request and '__ac_password' in request:
            return {
                'src': self.getId(),
                'login': request.get('__ac_name'),
                'password': request.get('__ac_password')
            }

    security.declarePrivate('authenticateCredentials')

    def authenticateCredentials(self, credentials):
        """ We expect that credentials will be returned by
          extractCredentials.
        """
        if credentials.get('src') != self.getId():
            return

        login = credentials.get('login')
        password = credentials.get('password')

        if login is None or password is None:
            return None
        # check credentials using a wikid server
        connector = self._getWikidConnection()
        result = connector.login(login, password, self.domaincode)
        if result is True:
            return login, login
