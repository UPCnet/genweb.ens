# -*- coding: utf-8 -*-

from mock import Mock
import json
from transaction import commit

from plone.testing.z2 import Browser
from plone import api

from genweb.ens.testing import FunctionalTestCase
from genweb.ens.tests.fixtures import fixtures, dummy


class TestTaulaViews(FunctionalTestCase):
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

    def get_folders_query_string(self, folders):
        folder_paths = [folder.absolute_url_path()
                        for folder in folders]
        return '?carpetes=' + json.dumps(folder_paths)

    def test_taula_identificativa(self):
        folder_1 = fixtures.create_content(self.portal, fixtures.folder_1)
        folder_2 = fixtures.create_content(self.portal, fixtures.folder_2)
        ens_1 = fixtures.create_content(folder_1, fixtures.ens_1)
        ens_2 = fixtures.create_content(folder_1, fixtures.ens_2)
        ens_3 = fixtures.create_content(folder_2, fixtures.ens_incomplete)
        commit()

        view = api.content.get_view('taula_identificativa',
                                    self.layer['portal'],
                                    self.layer['request'])

        # Test that ens in folder-1 are shown in alphabetical order
        folder_list = [folder_1]
        self.browser.open((view.url() +
                           self.get_folders_query_string(folder_list)))

        self.assertAppearInOrder([
            ens_1.title.encode('utf8'),
            ens_2.title.encode('utf8')],
            self.browser.contents)
        self.assertNotIn(ens_3.title.encode('utf-8'), self.browser.contents)

        # Test that ens in folder-2 are shown in alphabetical order
        folder_list = [folder_2]
        self.browser.open((view.url() +
                           self.get_folders_query_string(folder_list)))

        self.assertIn(ens_3.title.encode('utf8'), self.browser.contents)
        self.assertNotIn(ens_1.title.encode('utf-8'), self.browser.contents)
        self.assertNotIn(ens_2.title.encode('utf-8'), self.browser.contents)

        # Test that ens in both foler-1 and folder-2 are shown in alphabetical
        # order
        folder_list = [folder_1, folder_2]
        self.browser.open((view.url() +
                           self.get_folders_query_string(folder_list)))

        self.assertIn(ens_3.title.encode('utf8'), self.browser.contents)
        self.assertAppearInOrder([
            ens_3.title.encode('utf8'),
            ens_1.title.encode('utf8'),
            ens_2.title.encode('utf8')],
            self.browser.contents)

        # Test that ens in all folders are shown in alphabetical order if no
        # folder is specified
        self.browser.open(view.url())
        self.assertAppearInOrder([
            ens_3.title.encode('utf8'),
            ens_1.title.encode('utf8'),
            ens_2.title.encode('utf8')],
            self.browser.contents)

        # Test that no ens are shown if a nonexistent folder is specified
        folder_list = [
            Mock(absolute_url_path=Mock(side_effect=('/nonexistent/path',)))]

        self.browser.open((view.url() +
                           self.get_folders_query_string(folder_list)))
        self.assertNotIn(ens_1.title.encode('utf-8'), self.browser.contents)
        self.assertNotIn(ens_2.title.encode('utf-8'), self.browser.contents)
        self.assertNotIn(ens_3.title.encode('utf-8'), self.browser.contents)

    def test_taula_representacio(self):
        folder_1 = fixtures.create_content(self.portal, fixtures.folder_1)
        folder_1_titles = []
        for ens_number in (1, 2):
            ens = dummy.create_ens(folder_1, ens_number)
            for organ_type in ('Govern', 'Assessor'):
                for organ_num in (1, 2):
                    organ = dummy.create_organ(ens, organ_type, organ_num)
                    for carrec_num in (1, 2):
                        for persona_num in (1, 2):
                            carrec = dummy.create_carrec(
                                organ,
                                ens_number, organ_type, organ_num,
                                carrec_num, persona_num)
                            dummy.create_carrec(
                                organ,
                                ens_number, organ_type, organ_num,
                                carrec_num, persona_num, is_historic=True)
                            folder_1_titles.append(
                                carrec.title.encode('utf-8'))

        folder_2 = fixtures.create_content(self.portal, fixtures.folder_2)
        folder_2_titles = []
        for ens_number in (3,):
            ens = dummy.create_ens(folder_2, ens_number)
            for organ_type in ('Govern', 'Assessor'):
                for organ_num in (1, 2):
                    organ = dummy.create_organ(ens, organ_type, organ_num)
                    for carrec_num in (1, 2):
                        for persona_num in (1, 2):
                            carrec = dummy.create_carrec(
                                organ,
                                ens_number, organ_type, organ_num,
                                carrec_num, persona_num)
                            folder_2_titles.append(
                                carrec.title.encode('utf-8'))
        commit()

        view = api.content.get_view('taula_representacio',
                                    self.layer['portal'],
                                    self.layer['request'])

        # Test that ens in folder-1 are shown in alphabetical order
        folder_list = [folder_1]
        self.browser.open((view.url() +
                           self.get_folders_query_string(folder_list)))

        self.assertAppearInOrder(folder_1_titles, self.browser.contents)
        for title in folder_2_titles:
            self.assertNotIn(title, self.browser.contents)

        # Test that ens in folder-2 are shown in alphabetical order
        folder_list = [folder_2]
        self.browser.open((view.url() +
                           self.get_folders_query_string(folder_list)))

        self.assertAppearInOrder(folder_2_titles, self.browser.contents)
        for title in folder_1_titles:
            self.assertNotIn(title, self.browser.contents)

        # Test that ens in both folder-1 and folder-2 are shown in alphabetical
        # order
        folder_list = [folder_1, folder_2]
        self.browser.open((view.url() +
                           self.get_folders_query_string(folder_list)))

        folder_1_2_titles = folder_1_titles + folder_2_titles
        self.assertAppearInOrder(folder_1_2_titles, self.browser.contents)

        # Test all ens are shown in alphabetical order when no folder specified
        folder_list = [folder_1, folder_2]
        self.browser.open(view.url())

        folder_1_2_titles = folder_1_titles + folder_2_titles
        self.assertAppearInOrder(folder_1_2_titles, self.browser.contents)

        # Test that no ens are shown if a nonexistent folder is specified
        folder_list = [
            Mock(absolute_url_path=Mock(side_effect=('/nonexistent/path',)))]
        self.browser.open((view.url() +
                           self.get_folders_query_string(folder_list)))
        for title in folder_1_2_titles:
            self.assertNotIn(title, self.browser.contents)
