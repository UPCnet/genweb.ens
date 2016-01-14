# -*- coding: utf-8 -*-

"""Integration tests for taula views."""
import os
from StringIO import StringIO

from plone import api

from genweb.ens.testing import IntegrationTestCase
from genweb.ens.tests.fixtures import fixtures


class TestTaulaViews(IntegrationTestCase):
    """Test taula views functions."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.folder_files_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'files')

    def test_taula_identificativa_csv_write_data(self):
        fixtures.create_content(self.layer['portal'], fixtures.ens_1)
        fixtures.create_content(self.layer['portal'], fixtures.ens_2)
        fixtures.create_content(self.layer['portal'], fixtures.ens_incomplete)

        view = api.content.get_view("taula_identificativa_csv",
                                    self.layer['portal'],
                                    self.layer['request'])
        csv_file = StringIO()
        view.write_data(csv_file)
        csv_file_contents = csv_file.getvalue()
        csv_file.close()

        file_taula_identificativa_path = os.path.join(
            self.folder_files_path, 'taula_identificativa.csv')
        with open(file_taula_identificativa_path) as csv_file_reference:
            self.assertEqual(csv_file_reference.read(), csv_file_contents)

    def test_taula_representacio_csv_write_data(self):
        ens = fixtures.create_content(self.layer['portal'], fixtures.ens_1)
        organ = fixtures.create_content(ens, fixtures.organ_1)
        fixtures.create_content(organ, fixtures.carrec_1)
        fixtures.create_content(organ, fixtures.carrec_2)
        fixtures.create_content(self.layer['portal'], fixtures.ens_2)

        view = api.content.get_view("taula_representacio_csv",
                                    self.layer['portal'],
                                    self.layer['request'])
        csv_file = StringIO()
        view.write_data(csv_file)
        csv_file_contents = csv_file.getvalue()
        csv_file.close()

        file_taula_representacio_path = os.path.join(
            self.folder_files_path, 'taula_representacio.csv')
        with open(file_taula_representacio_path) as csv_file_reference:
            self.assertEqual(csv_file_reference.read(), csv_file_contents)
