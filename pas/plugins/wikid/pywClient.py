''' wClient.py
Python Client for wikid '''

import re
import socket
import logging
from select import select
from functools import wraps
from OpenSSL import *
from xml.dom import minidom, Node

from wauth import\
    (PING, CONNECT, REGISTRATION, LIST_USERS,
     LOGIN, FIND_USER, DELETE, LIST_DOMAINS)

__author__ = "Manish Rai Jain <manishrjain@gmail.com>"

CLIENT_ID = "WiKID Python Client v4.0"

logger = logging.getLogger(__name__)


def verify_cb(conn, cert, errnum, depth, ok):
    """ It should return true if verification passes and false otherwise.
    """
    return ok


def prepare_xml_srting(s):
    return re.sub(r'\s+', ' ', s) + '\n'


def get_tag_data(xmltree, tag_name, index=0):
    """ It gets data from a tag """
    return xmltree.getElementsByTagName(tag_name)[index].firstChild.data


class pywClient:

    def __init__(self, host=None, port=None, pkey=None, passPhrase=None,
                 caCert=None):
        """ This will create a SSL Connection b/w client and server.
        :param host: IP address of WIKID server
        :type host: string
        :param port: TCP port number to connect to (default 8388)
        :type port: string
        :param pkey: A path to the PKCS12 certificate file
        :type pkey: string
        :param passPhrase: a passphrase to open the PKCS12 file
        :type passPhrase: string
        :param caCert: - a path to certificate for validating
            the WAS server certificate.
        :type caCert: string
        """

        self.host = host
        self.port = port
        self.pkey = pkey
        self.passPhrase = passPhrase
        self.cacert = caCert

        ctx = SSL.Context(SSL.SSLv3_METHOD)
        ctx.set_verify(SSL.VERIFY_PEER, verify_cb)
        ctx.set_verify(SSL.VERIFY_NONE, verify_cb)
        ctx.load_verify_locations(None, self.cacert)

        # Get X509 certificate and the private key from the
        # initial .p12 file provided to network client
        f = open(pkey)

        pkcs12Obj = crypto.load_pkcs12(f.read(), passPhrase)
        pkeyObj = pkcs12Obj.get_privatekey()
        x509Obj = pkcs12Obj.get_certificate()

        ctx.use_privatekey(pkeyObj)
        ctx.use_certificate(x509Obj)

        self.sock = SSL.Connection(
            ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))

    def assure_connection(f):
        @wraps(f)
        def ensure_connection(self, *args, **kw):
            try:
                self.request(prepare_xml_srting(PING))
            except SSL.Error:
                self.establishSSLConnection()
            return f(self, *args, **kw)
        return ensure_connection

    def establishSSLConnection(self):
        logger.debug("Connecting...")
        self.sock.connect((self.host, self.port))
        logger.debug("Connected. Trying Handshake...")
        self.sock.do_handshake()
        logger.debug("Handshaking done.")

    def xmlrequest(self, message):
        """ Send XML request over the socket and return the XML response.
        """
        message = prepare_xml_srting(message)
        response = self.request(message + "\n")
        if response:
            doc = minidom.parseString(response)
            return doc.documentElement

    def request(self, message=None):
        """ Send request over the socket and return the response.
        """
        timeout = 2
        response = ''

        logger.debug('Sending request: ' + message)
        sent = self.sock.send(message)
        if sent == 0:
            raise RuntimeError("socket connection broken")

        self.sock.setblocking(0)
        ready = select([self.sock], [], [], timeout)
        if ready[0]:
            while not response.endswith("\n"):
                try:
                    chunk = self.sock.recv(8192)
                except SSL.WantReadError:
                    continue
                if chunk:
                    response = response + chunk
                else:
                    break
        logger.debug('Response received: ' + response)
        return response

    @assure_connection
    def ping(self):
        """ Send a ping to the server, to make sure it's open """
        return self.xmlrequest(PING)

    @assure_connection
    def checkCredentials(self, user='null', domaincode='null',
                         passcode='null', challenge='null', response='null'):
        """ This method returns a boolean representing successful or
            unsuccessful authentication.
        :param user: userid to validate credentials.
        :type user: string
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
        return self.verify("base", user, domaincode, passcode, challenge,
                           response, chap_password='null',
                           chap_challenge='null', wikid_challenge=None)

    def verify(self, format, user='null', domaincode='null', passcode='null',
               challenge='null', response='null', chap_password='null',
               chap_challenge='null', wikid_challenge='null'):
        """ This helper method verifies credentials using
           the specified mechanism
        """

        message = LOGIN % locals()
        return 'VALID' == get_tag_data(self.xmlrequest(message), 'result')

    def chapVerify(self, user=None, domaincode=None, chap_password=None,
                   chap_challenge=None, wikid_challenge=None):

        if wikidChallenge is None:
            format = "chapOff"
        else:
            format = "chap"

        return self.verify(user, format, domaincode, passcode, '', '',
                           chap_password, chap_challenge, wikid_challenge)

    @assure_connection
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

    @assure_connection
    def connect(self):
        """ Authentication procedure completed.
           Start off connection with the server now.
        """
        logger.info("Start Connection...")
        message = CONNECT % {'client': CLIENT_ID}
        return get_tag_data(self.xmlrequest(message), 'result') == 'ACCEPT'

    def getDomains(self):
        """ Get all domains from the wikid server """
        response = self.xmlrequest(LIST_DOMAINS)
        return response.getElementsByTagName("domain-list")

    def listUsers(self, domaincode=None):
        """ List users that refer to the domain. """
        message = LIST_USERS % locals()
        response = self.xmlrequest(message)
        return response.getElementsByTagName('user-id')

    def login(
            self, format, user, passcode, domaincode=None,
            challenge=None, response=None,
            chap_password=None, chap_challenge=None,
    ):
        """ Sign in to the wikid server """
        message = LOGIN % locals()
        return self.xmlrequest(message)

    def findUser(self, user, domaincode, returncode):
        """ It gets a lot of information about the user """
        message = FIND_USER % locals()
        return self.xmlrequest(message)

    def deleteUser(self, user, domaincode, returncode):
        """ Delete a user from the wikid server """
        user_info = self.xmlrequest(FIND_USER % locals())
        user_tag = user_info.getElementsByTagName('user')[0].toxml()
        message = DELETE % locals()
        result = get_tag_data(self.xmlrequest(message), 'result')
        return result in ('SUCCESS', 'SUCESS')
