# -*- coding: utf-8 -*-

from urllib2 import HTTPError
from transaction import commit

from plone.testing.z2 import Browser
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD

from genweb.ens.testing import FunctionalTestCase
from genweb.ens.tests.fixtures import fixtures


class TestCarrecSearch(FunctionalTestCase):
    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.browser = Browser(self.portal)

    def assertAppearsBefore(self, subtxt_1, subtxt_2, txt):
        self.assertIn(subtxt_1, txt)
        self.assertIn(subtxt_2, txt)
        self.assertTrue(txt.find(subtxt_1) < txt.find(subtxt_2))

    def assertAppearInOrder(self, subtxts, txt):
        def assertAppearsBefore(subtxt_1, subtxt_2):
            self.assertAppearsBefore(subtxt_1, subtxt_2, txt)
            return subtxt_2
        reduce(assertAppearsBefore, subtxts)

    def login(self):
        self.browser.getControl(
            name='__ac_name').value = SITE_OWNER_NAME
        self.browser.getControl(
            name='__ac_password').value = SITE_OWNER_PASSWORD
        self.browser.getControl(name='submit').click()

    def test_add_carrec_when_duplicated_representants(self):
        # Given 2 representants with the same id but in different folders
        folder_consell_direccio = fixtures.create_content(
            self.portal, fixtures.folder_consell_direccio)
        folder_altres = fixtures.create_content(
            self.portal, fixtures.folder_altres)
        fixtures.create_content(
            folder_consell_direccio, fixtures.representant_1)
        fixtures.create_content(folder_altres, fixtures.representant_1_bis)
        commit()

        # The add form of carrec_upc shows both representants in the selection
        # field
        try:
            self.browser.open(
                api.portal.get().absolute_url() +
                '/++add++genweb.ens.carrec_upc')
            self.login()
        except HTTPError:
            pass
        self.assertEquals('200 Ok', self.browser.headers['status'])
        self.assertIn(fixtures.representant_1['id'], self.browser.contents)
        self.assertIn(fixtures.representant_1_bis['id'], self.browser.contents)
