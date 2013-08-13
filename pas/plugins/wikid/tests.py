import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

import pas.plugins.wikid

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             pas.plugins.wikid)
            fiveconfigure.debug_mode = False
            # This is only necessary for packages outside the Products.* namespace
            # which are also declared as Zope 2 products, using
            # <five:registerPackage /> in ZCML. See 'pas/plugins/wikid/configure.zcml'.
            ztc.installPackage('pas.plugins.wikid')

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            'README.txt', package='pas.plugins.wikid',
            test_class=TestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
