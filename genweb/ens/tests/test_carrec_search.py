# -*- coding: utf-8 -*-

from mock import Mock
import json
from transaction import commit

from plone.testing.z2 import Browser
from plone import api

from genweb.ens.testing import FunctionalTestCase
from genweb.ens.tests.fixtures import fixtures, dummy


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

    def get_query_string(self, text, folders, historics):
        folder_paths = [folder.absolute_url_path()
                        for folder in folders]
        return '?text={0}&carpetes={1}&historics={2}'.format(
            text,
            json.dumps(folder_paths),
            'true' if historics else 'false')

    def test_search_results(self):
        folder_1 = fixtures.create_content(self.portal, fixtures.folder_1)
        folder_1_titles_nonhistorics = []
        folder_1_titles_historics = []
        folder_1_titles_all = []
        for ens_number in (1, 2):
            ens = dummy.create_ens(folder_1, ens_number)
            for organ_type in ('Govern', 'Assessor'):
                for organ_num in (1, 2):
                    organ = dummy.create_organ(ens, organ_type, organ_num)
                    for carrec_num in (1, 2):
                        for persona_num in (1, 2):
                            carrec_nonhistoric = dummy.create_carrec(
                                organ,
                                ens_number, organ_type, organ_num,
                                carrec_num, persona_num)
                            carrec_historic = dummy.create_carrec(
                                organ,
                                ens_number, organ_type, organ_num,
                                carrec_num, persona_num, is_historic=True)
                            folder_1_titles_nonhistorics.append(
                                carrec_nonhistoric.title.encode('utf-8'))
                            folder_1_titles_historics.append(
                                carrec_historic.title.encode('utf-8'))
                            folder_1_titles_all.append(
                                carrec_nonhistoric.title.encode('utf-8'))
                            folder_1_titles_all.append(
                                carrec_historic.title.encode('utf-8'))

        folder_2 = fixtures.create_content(self.portal, fixtures.folder_2)
        folder_2_titles_all = []
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
                            folder_2_titles_all.append(
                                carrec.title.encode('utf-8'))
        commit()

        view = api.content.get_view('carrec_search_results',
                                    self.layer['portal'],
                                    self.layer['request'])

        # Test that carrecs in folder-1 are shown in alphabetical order
        folder_list = [folder_1]

        # Test when text is empty and historics=False
        self.browser.open((view.url() +
                           self.get_query_string('', folder_list, False)))

        self.assertAppearInOrder(
            sorted(folder_1_titles_nonhistorics), self.browser.contents)
        for title in folder_1_titles_historics:
            self.assertNotIn(title, self.browser.contents)

        for title in folder_2_titles_all:
            self.assertNotIn(title, self.browser.contents)

        # Test when text is empty and historics=True
        self.browser.open((view.url() +
                           self.get_query_string('', folder_list, True)))

        self.assertAppearInOrder(
            sorted(folder_1_titles_all), self.browser.contents)

        for title in folder_2_titles_all:
            self.assertNotIn(title, self.browser.contents)

        # Test when text is not empty and historics=False
        text = 'Persona 01'
        self.browser.open((view.url() +
                           self.get_query_string(text, folder_list, False)))

        self.assertAppearInOrder(
            sorted(
                [title for title in folder_1_titles_nonhistorics
                 if title.startswith(text)]),
            self.browser.contents)
        for title in [title for title in folder_1_titles_nonhistorics
                      if not title.startswith(text)]:
            self.assertNotIn(title, self.browser.contents)

        for title in folder_1_titles_historics:
            self.assertNotIn(title, self.browser.contents)

        for title in folder_2_titles_all:
            self.assertNotIn(title, self.browser.contents)

        # Test when text is not empty and historics=True
        text = 'Persona 01'
        self.browser.open((view.url() +
                           self.get_query_string(text, folder_list, True)))

        self.assertAppearInOrder(
            sorted(
                [title for title in folder_1_titles_all
                 if title.startswith(text)]),
            self.browser.contents)

        for title in [title for title in folder_1_titles_all
                      if not title.startswith(text)]:
            self.assertNotIn(title, self.browser.contents)

        for title in folder_2_titles_all:
            self.assertNotIn(title, self.browser.contents)

        # Test that ens in folder-2 are shown in alphabetical order
        folder_list = [folder_2]
        self.browser.open((view.url() +
                           self.get_query_string('', folder_list, False)))

        self.assertAppearInOrder(
            sorted(folder_2_titles_all), self.browser.contents)
        for title in folder_1_titles_all:
            self.assertNotIn(title, self.browser.contents)

        # Test that ens in both folder-1 and folder-2 are shown in alphabetical
        # order
        folder_list = [folder_1, folder_2]
        self.browser.open((view.url() +
                           self.get_query_string('', folder_list, False)))

        folder_1_2_titles = folder_1_titles_nonhistorics + folder_2_titles_all
        self.assertAppearInOrder(
            sorted(folder_1_2_titles), self.browser.contents)

        # Test all ens are shown in alphabetical order when no folder specified
        self.browser.open(view.url())

        folder_1_2_titles = folder_1_titles_nonhistorics + folder_2_titles_all
        self.assertAppearInOrder(
            sorted(folder_1_2_titles), self.browser.contents)

        # Test that no ens are shown if a nonexistent folder is specified
        folder_list = [
            Mock(absolute_url_path=Mock(side_effect=('/nonexistent/path',)))]
        self.browser.open((view.url() +
                           self.get_query_string('', folder_list, False)))
        for title in folder_1_2_titles:
            self.assertNotIn(title, self.browser.contents)
