""" It's dedicated to enumeration plugins """
import copy
from itertools import ifilter

from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin
from Products.PluggableAuthService.utils import createViewName


class UserEnumerator(object):
    """ It's a mixin for WiKIDAuthMultiPlugin
    """
    implements(IUserEnumerationPlugin)
    meta_type = 'WiKID User Enumeration Plugin'
    security = ClassSecurityInfo()

    security.declarePrivate('enumerateUsers')

    def getUsers(self):
        """ Get users from a wikid server """
        connector = self._getWikidConnection()
        users = (user for user in connector.listUsers(self.domaincode))
        info = lambda user: {
            'id': user,
            'login': user,
            'pluginid': self.getId()
        }
        return (info(user) for user in users)

    def enumerateUsers(self, id=None, login=None, exact_match=False,
                       sort_by=None, max_results=None, **kw):
        # we don't support search by e-mail and fullname for now
        if 'email' in kw or 'fullname' in kw:
            return ()

        username = login or id

        def getRAMKeys():
            keywords = copy.deepcopy(kw)
            info = {
                'plugin_id': self.getId(),
                'id_or_login': username,
                'sort_by': sort_by,
                'exact_match': exact_match,
                'max_results': max_results,
            }
            keywords.update(info)
            return keywords

        # Check cached data
        view_name = createViewName('enumerateUsers')
        keys = getRAMKeys()
        user_info = self.ZCacheable_get(
            view_name=view_name,
            keywords=keys,
        )
        if user_info is not None:
            return user_info
        # get user fields
        user_fields = self.getUsers()
        if exact_match:
            user_fields = ifilter(lambda user: username == user.get('id'), user_fields)
        # Cache data upon success
        retvalues = list(user_fields)
        self.ZCacheable_set(retvalues, view_name=view_name, keywords=keys)
        return retvalues
