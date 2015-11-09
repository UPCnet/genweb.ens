# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from genweb.ens.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of genweb.ens into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if genweb.ens is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('genweb.ens'))

    def test_uninstall(self):
        """Test if genweb.ens is cleanly uninstalled."""
        self.installer.uninstallProducts(['genweb.ens'])
        self.assertFalse(self.installer.isProductInstalled('genweb.ens'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IGenwebEnsLayer is registered."""
        from genweb.ens.interfaces import IGenwebEnsLayer
        from plone.browserlayer import utils
        self.failUnless(IGenwebEnsLayer in utils.registered_layers())
