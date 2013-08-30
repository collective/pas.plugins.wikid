""" It's dedicated to enumeration plugins """
from itertools import ifilter

from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin


class UserEnumerator(object):
    """ It's a mixin for WiKIDAuthMultiPlugin
    """
    implements(IUserEnumerationPlugin)
    meta_type = 'WiKID User Enumeration Plugin'
    security = ClassSecurityInfo()

    security.declarePrivate('enumerateUsers')

    def enumerateUsers(self, id=None, login=None, exact_match=False,
                       sort_by=None, max_results=None, **kw):
        connector = self._getWikidConnection()
        users = (user for user in connector.listUsers(self.domaincode))
        info = lambda user: {
            'id': user,
            'login': user,
            'pluginid': self.getId()
        }
        result = (info(user) for user in users)
        if exact_match:
            key = login or id
            result = ifilter(lambda user: key == user.get('id'), result)
        return tuple(result)
