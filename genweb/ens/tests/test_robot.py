import unittest

import robotsuite
from genweb.ens.testing import ROBOT_TESTING
from plone.testing import layered


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('./robot/'
                'test_ens_is_installed.robot'),
                layer=ROBOT_TESTING),
        layered(robotsuite.RobotTestSuite('./robot/'
                'test_search_ens.robot'),
                layer=ROBOT_TESTING),
    ])
    return suite
