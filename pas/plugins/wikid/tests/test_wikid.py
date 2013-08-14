""" It tests the python wikid client. """

import unittest
import logging
from pas.plugins.wikid.pywClient import pywClient


# Please set up this options for testing. See 'pas/plugins/wikid/example.py' for details.
# Options that refer to a wikid server.
HOST = '127.0.0.1'
DOMAINCODE = '127000000001'
PORT = 8388
PKEY = 'localhost.p12'
WIKID_SERVER_PASSCODE = 'secret'
CACERT = 'CACertStore'
# Options that refer to a wikid user.
USER = 'testuser'
PASSCODE = 'passcode'
REGCODE = 'regcode'


class TestWikidClient(unittest.TestCase):
    """ It tests the python wikid client. """

    def setUp(self):
        self.client = pywClient(
            host=HOST,
            port=PORT,
            pkey=PKEY,
            passPhrase=WIKID_SERVER_PASSCODE,
            caCert=CACERT
        )

    def test_registration(self):
        # Set up the connection
        self.assertTrue(self.client.startConnection())
        # Validate the user
        self.assertEqual(
            2,    #TODO: rewrite 'registerUsername'
            self.client.registerUsername(
                user=USER, regcode=REGCODE, domaincode=DOMAINCODE
            )
        )
        # Check user's credentials
        self.assertTrue(
            self.client.checkCredentials(
                user=USER,
                domaincode=DOMAINCODE,
                passcode=PASSCODE,
            )
        )


if __name__ == '__main__':
    # Set up the logging level for testing.
    logger = logging.getLogger('pywClient')
    logger.addHandler(logging.StreamHandler())
    # 'logging.DEBUG' to get more details
    logger.setLevel(logging.INFO)
    # Run tests
    unittest.main()
