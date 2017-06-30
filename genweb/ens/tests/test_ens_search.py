# -*- coding: utf-8 -*-

import json
from transaction import commit

from plone.testing.z2 import Browser
from plone import api

from genweb.ens.testing import FunctionalTestCase
from genweb.ens.tests.fixtures import fixtures, dummy


class TestEnsSearch(FunctionalTestCase):
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

    def get_query_string(self, figura_juridica, estat, folders, text):
        folder_paths = [folder.absolute_url_path()
                        for folder in folders]
        return '?figura_juridica={0}&estat={1}&carpetes={2}&text={3}'.format(
            figura_juridica,
            estat,
            json.dumps(folder_paths),
            text)

    def test_search_results(self):
        # Create the following contents:
        # folder  title   fig.jur.  estat                 description
        # 1       Ens 01  Fundació  Pre-Alta cancel·lada  desc-a
        # 1       Ens 02  Fundació  Pre-Alta cancel·lada  desc-b
        # 1       Ens 03  Fundació  Alta                  desc-a
        # 1       Ens 04  Fundació  Alta                  desc-b
        folder_1 = fixtures.create_content(self.portal, fixtures.folder_1)
        ens_list = []
        for figura_juridica in (u'Fundació',):
            for estat in (
                    u'Pre-Alta cancel·lada',
                    u'Alta'):
                for description in (u'desc-a', u'desc-b'):
                    ens_list.append(dummy.create_ens(
                        folder_1,
                        len(ens_list) + 1,
                        figura_juridica=figura_juridica,
                        estat=estat,
                        description=description))

        # Create the following contents:
        # folder  title   fig.jur.  estat      description
        # 1       Ens 05  Societat  Pre-Baixa  desc-a
        # 1       Ens 06  Societat  Pre-Baixa  desc-b
        # 1       Ens 07  Societat  Pre-Alta   desc-a
        # 1       Ens 08  Societat  Pre-Alta   desc-b
        for figura_juridica in (u'Societat',):
            for estat in (
                    u'Pre-Baixa',
                    u'Pre-Alta'):
                for description in (u'desc-a', u'desc-b'):
                    ens_list.append(dummy.create_ens(
                        folder_1,
                        len(ens_list) + 1,
                        figura_juridica=figura_juridica,
                        estat=estat,
                        description=description))

        # Create the following contents:
        # folder  title   fig.jur.  estat  description
        # 2       Ens 09  Consorci  Baixa  desc-c
        folder_2 = fixtures.create_content(self.portal, fixtures.folder_2)
        ens_list.append(dummy.create_ens(
            folder_2,
            len(ens_list) + 1,
            figura_juridica=u'Consorci',
            estat=u'Baixa',
            description=u'des-c'))
        commit()

        view = api.content.get_view('ens_search_results',
                                    self.layer['portal'],
                                    self.layer['request'])

        # Test that carrecs in folder-1 are shown in alphabetical order
        folder_list = [folder_1]

        # Test filtering by figura jurídica
        self.browser.open((view.url() +
                           self.get_query_string(
                               'Fundació',
                               '',
                               folder_list,
                               '')))

        self.assertAppearInOrder(
            [ens.title.encode('utf-8') for ens in ens_list[:4]],
            self.browser.contents)
        for title in [ens.title.encode('utf-8') for ens in ens_list[4:]]:
            self.assertNotIn(title, self.browser.contents)

        # Test filtering by figura jurídica and estat
        self.browser.open((view.url() +
                           self.get_query_string(
                               'Fundació',
                               'Pre-Alta cancel·lada',
                               folder_list,
                               '')))

        self.assertAppearInOrder(
            [ens.title.encode('utf-8') for ens in ens_list[:2]],
            self.browser.contents)
        for title in [ens.title.encode('utf-8') for ens in ens_list[2:]]:
            self.assertNotIn(title, self.browser.contents)

        # Test filtering by figura jurídica, estat and text
        self.browser.open((view.url() +
                           self.get_query_string(
                               'Fundació',
                               'Pre-Alta cancel·lada',
                               folder_list,
                               'desc-a')))

        self.assertAppearInOrder(
            [ens.title.encode('utf-8') for ens in ens_list[:1]],
            self.browser.contents)
        for title in [ens.title.encode('utf-8') for ens in ens_list[1:]]:
            self.assertNotIn(title, self.browser.contents)

        # Test that carrecs in folder-2 are shown in alphabetical order
        folder_list = [folder_2]

        self.browser.open((view.url() +
                           self.get_query_string('', '', folder_list, '')))

        self.assertIn(
            ens_list[-1].title.encode('utf-8'), self.browser.contents)
        for title in [ens.title.encode('utf-8') for ens in ens_list[:-1]]:
            self.assertNotIn(title, self.browser.contents)
