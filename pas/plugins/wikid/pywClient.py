""" The client for wikid """

import re
import logging
from functools import wraps
from xml.dom import minidom
from OpenSSL import SSL

from wauth import\
    (PING, CONNECT, REGISTRATION, LIST_USERS, ADD_PRE_REGISTRATION_CODE,
     LOGIN, FIND_USER, DELETE, LIST_DOMAINS, PRE_REGISTRATION, REPORT,
     DELETE_BY_DEVICE_ID, LIST_REGCODES)

from connection import SSLConnector

CLIENT_ID = "WiKID Python Client v4.0"

logger = logging.getLogger(__name__)


def prepare_xml_srting(s):
    return re.sub(r'\s+', ' ', s) + '\n'


def get_tag_data(xmltree, tag_name, index=0):
    """ It gets data from a tag """
    return xmltree.getElementsByTagName(tag_name)[index].firstChild.data


class pywClient(SSLConnector):
    def __init__(self, **ssl_settings):
        super(pywClient, self).__init__(**ssl_settings)

    def xmlrequest(self, message):
        """ Send XML request over the socket and return the XML response.
        """
        message = prepare_xml_srting(message)
        response = self.request(message)
        if response:
            doc = minidom.parseString(response)
            return doc.documentElement

    def __assure_connection(f):
        @wraps(f)
        def ensure_connection(self, *args, **kw):
            try:
                self.xmlrequest(prepare_xml_srting(PING))
            except SSL.Error:
                self.reconnect()
            return f(self, *args, **kw)
        return ensure_connection

    def ping(self):
        """ Send a ping to the server, to make sure it's open """
        return self.xmlrequest(PING)

    @__assure_connection
    def registerUsername(self, format, user=None, regcode=None, domaincode=None,
                         passcode=None, group=None):
        """ This method creates an association between the userid and
            the device registered by the user.
        :param user: userid with which to associate device
        :type user: string
        :param regcode: the registration code which you get from
            a token client (http://wikidsystems.com/downloads/token-clients).
        :type regcode: string
        :example regcode: '5Q4zvqIh'
        :param domaincode: the 12-digit code that represents the server/domain
        :type domaincode: string
        :param passcode: time-bounded, 1 use passcode.
            It's a code which you get when you use a token client
            (http://wikidsystems.com/downloads/token-clients).
        :type passcode: string
        :example passcode: '260328'
        """
        logger.info("The user (%s) is being registered." % user)
        message = REGISTRATION % locals()
        result = get_tag_data(self.xmlrequest(message), 'result')
        return result in ('SUCCESS', 'SUCESS')

    @__assure_connection
    def connect(self):
        """ Authentication procedure completed.
           Start off connection with the server now.
        """
        logger.info("Start Connection...")
        message = CONNECT % {'client': CLIENT_ID}
        return get_tag_data(self.xmlrequest(message), 'result') == 'ACCEPT'

    @__assure_connection
    def getDomains(self):
        """ Get all domains from the wikid server """
        response = self.xmlrequest(LIST_DOMAINS)
        return response.getElementsByTagName("domain-list")

    @__assure_connection
    def listUsers(self, domaincode=None):
        """ List users that refer to the domain. """
        message = LIST_USERS % locals()
        response = self.xmlrequest(message)
        return response.getElementsByTagName('user-id')

    @__assure_connection
    def login(
            self, user, passcode, domaincode, format='base',
            challenge=None, response=None,
            chap_password=None, chap_challenge=None,
    ):
        """ Sign in to the wikid server. This method returns
            a boolean representing successful or unsuccessful authentication.
        :param user: userid to validate credentials.
        :type user: string
        :param format: 'base' | 'chap' | 'chapoff' | 'offline'
        :param domaincode: the 12-digit code that represents the server/domain
        :type domaincode: string
        :param passcode: time-bounded, 1 use passcode.
            It's a code which you get when you use a token client
            (http://wikidsystems.com/downloads/token-clients).
        :type passcode: string
        :example passcode: '260328'
        :param challenge: the challenge value provided to the user
        :type challenge: string
        :param response: the hashed/signed response from the device
        :type response: string
        """
        message = LOGIN % locals()
        return 'VALID' == get_tag_data(self.xmlrequest(message), 'result')

    @__assure_connection
    def findUser(self, user, domaincode, returncode):
        """ It gets a lot of information about the user """
        message = FIND_USER % locals()
        return self.xmlrequest(message)

    @__assure_connection
    def deleteUser(self, user, domaincode, returncode):
        """ Delete a user from the wikid server """
        user_info = self.xmlrequest(FIND_USER % locals())
        user_tag = user_info.getElementsByTagName('user')[0].toxml()
        message = DELETE % locals()
        result = get_tag_data(self.xmlrequest(message), 'result')
        return result in ('SUCCESS', 'SUCESS')

    @__assure_connection
    def addPreRegistrationCode(self, user, prereg_code, domaincode, override='false'):
        """ Add a pre-registration code for the future registration. """
        message = ADD_PRE_REGISTRATION_CODE % locals()
        response = self.xmlrequest(message)
        logger.info(get_tag_data(response, 'result-message'))
        return get_tag_data(response, 'result') == 'true'

    @__assure_connection
    def preRegisterUser(self, regtoken, prereg_code, domaincode):
        """ Register a user using a pre-registration code """
        message = PRE_REGISTRATION % locals()
        response = self.xmlrequest(message)
        return get_tag_data(response, 'result') in ('SUCCESS', 'SUCESS')

    @__assure_connection
    def getReport(
            self,
            data_type='USER',   # Another option: 'DEVICE'
            separator=',',
            include_disable_users='false',
            include_token_data='false',
            group_user_data='false',
            include_disable_devices='false',
            include_unregistered='false',
    ):
        """ Get information according to the data_type """
        message = REPORT % locals()
        response = self.xmlrequest(message)
        return get_tag_data(response, 'reportData')

    @__assure_connection
    def deleteDeviceById(self, device_id, returncode):
        """ Delete a device by ID """
        message = DELETE_BY_DEVICE_ID % locals()
        response = self.xmlrequest(message)
        return get_tag_data(response, 'result') in ('SUCCESS', 'SUCESS')

    @__assure_connection
    def listRegCodes(self):
        """ List registration codes """
        response = self.xmlrequest(LIST_REGCODES)
        return response.getElementsByTagName('registrationCode')
