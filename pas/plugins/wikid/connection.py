""" It provides socket connections """

import time
import socket
import logging
from select import select
from OpenSSL import SSL, crypto


logger = logging.getLogger('pas.plugins.wikid.connection')


def verify_cb(conn, cert, errnum, depth, ok):
    """ It should return true if verification passes and false otherwise.
    """
    return ok


class SSLConnector(object):
    """ It connects and sends data through SSL """

    def __init__(self, host=None, port=None, pkey=None, pass_phrase=None,
                 cacert=None):
        """ This will create a SSL Connection b/w client and server.
        :param host: IP address of WIKID server
        :type host: string
        :param port: TCP port number to connect to (default 8388)
        :type port: string
        :param pkey: A path to the PKCS12 certificate file
        :type pkey: string
        :param pass_phrase: a passphrase to open the PKCS12 file
        :type pass_phrase: string
        :param cacert: - a path to certificate for validating
            the WAS server certificate.
        :type cacert: string
        """
        self.host = host
        self.port = port
        # set up the ssl context
        self.sslcontext = SSL.Context(SSL.SSLv3_METHOD)
        self.sslcontext.set_verify(SSL.VERIFY_PEER, verify_cb)
        self.sslcontext.set_verify(SSL.VERIFY_NONE, verify_cb)
        self.sslcontext.load_verify_locations(None, cacert)

        # Get X509 certificate and the private key from the
        # initial .p12 file provided to network client
        f = open(pkey)

        pkcs12Obj = crypto.load_pkcs12(f.read(), pass_phrase)
        pkeyObj = pkcs12Obj.get_privatekey()
        x509Obj = pkcs12Obj.get_certificate()

        self.sslcontext.use_privatekey(pkeyObj)
        self.sslcontext.use_certificate(x509Obj)

    def setUpSocket(self):
        """ Create a socket """
        self.socket = SSL.Connection(
            self.sslcontext, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def setUpConnection(self):
        """ Create a socket connection """
        self.setUpSocket()
        logger.debug("Connecting...")
        self.socket.connect((self.host, self.port))
        logger.debug("Connected. Trying Handshake...")
        self.socket.do_handshake()
        logger.debug("Handshaking done.")

    def closeConnection(self):
        """ Close a socket connection
            See for details: http://docs.python.org/2/howto/sockets.html#disconnecting
        """
        try:
            self.socket.shutdown()
        except SSL.Error:
            pass
        self.socket.close()

    def request(self, message, timeout=5):
        """ Send request over the socket and return the response.
        """
        logger.debug('Sending request: ' + message)
        sent = self.socket.send(message)
        if sent == 0:
            raise RuntimeError("socket connection broken")
        self.socket.setblocking(0)
        # wait for the first data in socket
        ready = select([self.socket], [], [], timeout)
        response = ''
        if ready[0]:
            recv_start_time = time.time()
            while True:
                if time.time() - recv_start_time >= timeout:
                    # prevent everlasting loop
                    break
                # See for details: http://docs.python.org/2/library/socket.html#socket.socket.recv
                try:
                    chunk = self.socket.recv(8192)
                except:
                    chunk = ""
                if chunk:
                    response += chunk
                else:
                    time.sleep(0.1)
                if '</transaction>' in response:
                    break
        logger.debug('Response received: ' + response)
        return response

    def reconnect(self):
        """ Recreate a socket connection """
        self.closeConnection()
        self.setUpConnection()
