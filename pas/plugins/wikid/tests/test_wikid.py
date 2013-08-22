""" It tests the python wikid client. """

import csv
import logging
import StringIO
import unittest2 as unittest

from pas.plugins.wikid.client import WikidClient, get_tag_data


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
# The pre-registration code
PRE_REG_CODE = '111111'
# It's a random value
RETURNCODE = 111

logger = logging.getLogger(__name__)


# Please note that the zope.testing test runner at the
# time of writing (version 3.9.3) does not (yet) support the new
# setUpClass(), tearDownClass(), setUpModule() and tearDownModule() hooks
# from unittest2.
class BaseLayer:
    @classmethod
    def setUp(cls):
        TestWikidClient.setUpClass()

    @classmethod
    def tearDown(cls):
        TestWikidClient.tearDownClass


class TestWikidClient(unittest.TestCase):
    """ It tests the python wikid client. """
    layer = BaseLayer

    @classmethod
    def setUpClass(cls):
        """ It's one-time process for all tests. """
        cls.client = WikidClient(
            host=HOST,
            port=PORT,
            pkey=PKEY,
            pass_phrase=WIKID_SERVER_PASSCODE,
            cacert=CACERT
        )
        cls.client.setUpConnection()
        # Register a new user according to REGCODE """
        if not cls.client.registerUsername(
            USER,
            REGCODE,
            DOMAINCODE
        ):
            logger.error("The user is not registrated so your tests will not work.")

    @classmethod
    def tearDownClass(cls):
        """ It's one-time process for all tests. """
        if not cls.client.deleteUser(
            USER,
            DOMAINCODE,
            RETURNCODE,
        ):
            logger.error("The user can't be deleted.")

# This methods can't be tested because they require a new REGCODE.
# See into 'setUpClass' - you will see that REGCODE is used.
# TODO: find a solution.
#    def test_addExtraDevice(self):
#        """ Add an extra device to a user. """
#        self.assertTrue(
#            self.client.registerUsername(
#                user=USER,
#                regcode=REGCODE,
#                passcode=PASSCODE,
#                domaincode=DOMAINCODE,
#                format='add',
#            )
#        )
#
#    def test_registerUsernameWithoutCheck(self):
#        """ Add a new user without checking existing. """
#        self.assertTrue(
#            self.client.registerUsername(
#                user=USER,
#                regcode=REGCODE,
#                domaincode=DOMAINCODE,
#                format='add-no-check',
#            )
#        )

    def test_checkCredentials(self):
        """ Validate a user by wikid server """
        self.assertTrue(
            self.client.login(
                USER,
                DOMAINCODE,
                PASSCODE,
            )
        )

    def test_ping(self):
        """ It tests the method 'ping' """
        response = self.client.ping()
        self.assertEqual(
            get_tag_data(response, 'value'),
            'ACK'
        )

    def test_listUsers(self):
        """ It's looking for the registered user in the user list.
        """
        users = self.client.listUsers(domaincode=DOMAINCODE)
        self.assertTrue(
            next(
                user
                for user in users
                if user.firstChild.data == USER
            )
        )

    def test_findUser(self):
        """ It's looking for a user name. """
        response = self.client.findUser(
            USER,
            DOMAINCODE,
            RETURNCODE,
        )
        self.assertEqual(
            get_tag_data(response, 'result'),
            'SUCESS',
        )

# The method can't be tested because it requires a new PASSCODE.
# See into 'test_checkCredentials' - you will see that PASSCODE is used.
# TODO: find a solution.
#    def test_online_login(self):
#        """ It tests the normal-state login for user. """
#        self.assertTrue(
#           self.client.login(
#               'base',
#               USER,
#               PASSCODE,
#               domaincode=DOMAINCODE
#           )

    def test_getDomains(self):
        """ Search for DOMAINCODE """
        domains = self.client.getDomains()
        self.assertTrue(
            next(
                domain
                for domain in domains
                if get_tag_data(domain, 'domaincode') == DOMAINCODE
            )
        )

# This methods can't be tested because it requires a new REGCODE.
# See into 'setUpClass' - you will see that REGCODE is used.
# TODO: find a solution.
#    def test_preRegistration(self):
#        """ Register USER using a pre-registration code """
#        # set the pre-registration code for a test-user
#        self.assertTrue(self.client.addPreRegistrationCode(USER, PRE_REG_CODE, DOMAINCODE))
#        # registration
#        self.assertTrue(
#            self.client.preRegisterUser(REGCODE, PRE_REG_CODE, DOMAINCODE)
#        )

    def test_getUsersReport(self):
        """ Search for USER in the report """
        self.assertTrue(USER in self.client.getReport())

# This methods can't be tested because it requires a new user name.
# TODO: find a solution. tested.
#    def test_deteteDeviceById(self):
#        """ Get a device by ID and delete it """
#        device_report = self.client.getReport(data_type='DEVICE')
#        device_id = next(
#            record.get('deviceid')
#            for record in csv.DictReader(StringIO.StringIO(device_report))
#            if USER == record.get('username')
#        )
#        self.assertTrue(
#            self.client.deleteDeviceById(device_id, RETURNCODE)
#        )

# This methods can't be tested because it requires a new REGCODE
# which has not been validated yet. See into
# 'setUpClass' - you will see that REGCODE is used.
# TODO: find a solution.
#    def test_listRegCodes(self):
#        """ Send LIST_REGCODES (wauth.py)- the piece of XML """
#        regcodes = self.client.listRegCodes()
#        self.assertTrue(
#            next(
#                regcode
#                for regcode in regcodes
#                if get_tag_data(regcode, 'regCode256') == REGCODE
#            )
#        )


if __name__ == '__main__':
    # Set up the logging level for testing.
    logger = logging.getLogger('pas.plugins.wikid.connection')
    logger.addHandler(logging.StreamHandler())
    # 'logging.DEBUG' to get more details
    logger.setLevel(logging.INFO)
    # BBB: We have to call this methods manually (Python < 2.7)
    # See details: http://docs.python.org/2/library/unittest.html#unittest.TestCase.setUpClass
    TestWikidClient.setUpClass()
    # Run tests
    unittest.main()
    TestWikidClient.tearDownClass()
