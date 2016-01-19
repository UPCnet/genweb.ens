# -*- coding: utf-8 -*-

"""Functional tests for static views."""

from plone.testing.z2 import Browser

from genweb.ens.testing import FunctionalTestCase


class TestStaticViews(FunctionalTestCase):
    """Test taula views functions."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.browser = Browser(self.layer['portal'])

    def test_homepage_navigation(self):
        self.browser.open(self.layer['portal'].absolute_url() + '/homepage')

        self.assertIn("Administrar representants UPC", self.browser.contents)
        self.assertIn("Taula identificativa", self.browser.contents)
        self.assertIn("Taula de representació", self.browser.contents)
        self.assertIn("Cercador de càrrecs", self.browser.contents)

        self.browser.getLink("Taula identificativa").click()
        self.assertIn("Taula identificativa", self.browser.contents)

        self.browser.goBack()
        self.browser.getLink("Taula de representació").click()
        self.assertIn("Taula de representació", self.browser.contents)

        self.browser.goBack()
        self.browser.getLink("Cercador de càrrecs").click()
        self.assertIn("Cercador de càrrecs", self.browser.contents)
