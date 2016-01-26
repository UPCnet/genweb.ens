# -*- coding: utf-8 -*-

"""Integration tests for taula CSV views."""

import os
from StringIO import StringIO
import json
from mock import Mock, patch

from plone import api

from genweb.ens.testing import IntegrationTestCase
from genweb.ens.tests.fixtures import fixtures, dummy


class TestTaulaCsvViews(IntegrationTestCase):
    def setUp(self):
        """Custom shared utility setup for tests."""
        self.folder_files_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'files')
        self.portal = self.layer['portal']

    def open_file(self, file_path):
        file_reference_path = os.path.join(
            self.folder_files_path, file_path)
        return open(file_reference_path)

    def taula_csv_get_data(self, view, folder_list=None):
        if folder_list:
            folder_paths = [folder.absolute_url_path()
                            for folder in folder_list]
            mocked_form = \
                Mock(get=Mock(side_effect=(json.dumps(folder_paths),)))
        else:
            mocked_form = view.request.form

        csv_file = StringIO()
        with patch.object(view.request, 'form', mocked_form):
            view.write_data(csv_file)
        csv_file_contents = csv_file.getvalue()
        csv_file.close()

        return csv_file_contents

    def test_taula_identificativa_csv_write_data(self):
        folder_1 = fixtures.create_content(self.portal, fixtures.folder_1)
        folder_2 = fixtures.create_content(self.portal, fixtures.folder_2)
        fixtures.create_content(folder_1, fixtures.ens_1)
        fixtures.create_content(folder_1, fixtures.ens_2)
        fixtures.create_content(folder_2, fixtures.ens_incomplete)

        view = api.content.get_view('taula_identificativa_csv',
                                    self.layer['portal'],
                                    self.layer['request'])

        # Test that only ens in folder-1 are written
        data = self.taula_csv_get_data(view, [folder_1])
        with self.open_file('taula_identificativa_f1.csv') as reference:
            self.assertEqual(reference.read(), data)

        # Test that only ens in folder-2 are written
        data = self.taula_csv_get_data(view, [folder_2])
        with self.open_file('taula_identificativa_f2.csv') as reference:
            self.assertEqual(reference.read(), data)

        # Test that ens in both folder-1 and folder-2 are written
        data = self.taula_csv_get_data(view, [folder_1, folder_2])
        with self.open_file('taula_identificativa_f1_f2.csv') as reference:
            self.assertEqual(reference.read(), data)

        # Test that ens all folders are written if no folder is specified
        data = self.taula_csv_get_data(view)
        with self.open_file('taula_identificativa_f1_f2.csv') as reference:
            self.assertEqual(reference.read(), data)

        # Test that no ens are written when a nonexistent folder is specified
        data = self.taula_csv_get_data(
            view,
            [Mock(absolute_url_path=Mock(side_effect=('/nonexistent/path',)))])
        with self.open_file('taula_identificativa_empty.csv') as reference:
            self.assertEqual(reference.read(), data)

    def test_taula_representacio_csv_write_data(self):
        folder_1 = fixtures.create_content(self.portal, fixtures.folder_1)
        for ens_number in (1, 2):
            ens = dummy.create_ens(folder_1, ens_number)
            for organ_type in ('Govern', 'Assessor'):
                for organ_num in (1, 2):
                    organ = dummy.create_organ(ens, organ_type, organ_num)
                    for carrec_num in (1, 2):
                        for persona_num in (1, 2):
                            dummy.create_carrec(
                                organ,
                                ens_number, organ_type, organ_num,
                                carrec_num, persona_num)
                            dummy.create_carrec(
                                organ,
                                ens_number, organ_type, organ_num,
                                carrec_num, persona_num, is_historic=True)

        folder_2 = fixtures.create_content(self.portal, fixtures.folder_2)
        for ens_number in (3,):
            ens = dummy.create_ens(folder_2, ens_number)
            for organ_type in ('Govern', 'Assessor'):
                for organ_num in (1, 2):
                    organ = dummy.create_organ(ens, organ_type, organ_num)
                    for carrec_num in (1, 2):
                        for persona_num in (1, 2):
                            dummy.create_carrec(
                                organ,
                                ens_number, organ_type, organ_num,
                                carrec_num, persona_num)

        view = api.content.get_view('taula_representacio_csv',
                                    self.layer['portal'],
                                    self.layer['request'])

        # Test that only ens in folder-1 are written
        data = self.taula_csv_get_data(view, [folder_1])
        with self.open_file('taula_representacio_f1.csv') as reference:
            self.assertEqual(reference.read(), data)

        # Test that only ens in folder-2 are written
        data = self.taula_csv_get_data(view, [folder_2])
        with self.open_file('taula_representacio_f2.csv') as reference:
            self.assertEqual(reference.read(), data)

        # Test that ens in both folder-1 and folder-2 are written
        data = self.taula_csv_get_data(view, [folder_1, folder_2])
        with self.open_file('taula_representacio_f1_f2.csv') as reference:
            self.assertEqual(reference.read(), data)

        # Test that all ens are written when no folder is specified
        data = self.taula_csv_get_data(view)
        with self.open_file('taula_representacio_f1_f2.csv') as reference:
            self.assertEqual(reference.read(), data)

        # Test that no ens are written when a nonexistent folder is specified
        data = self.taula_csv_get_data(
            view,
            [Mock(absolute_url_path=Mock(side_effect=('/nonexistent/path',)))])
        with self.open_file('taula_representacio_empty.csv') as reference:
            self.assertEqual(reference.read(), data)
