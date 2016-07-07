# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from datetime import datetime

from genweb.ens.testing import IntegrationTestCase
from genweb.ens.tests.fixtures import fixtures, dummy
from genweb.ens.data_access.ens import EnsDataReporter


class TestDataAccessIntegration(IntegrationTestCase):
    def setUp(self):
        self.portal = self.layer['portal']
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.reporter = EnsDataReporter(self.catalog)

    def test_list_by_contenidor_id_and_review_state(self):
        contenidor_1 = fixtures.create_content(
            self.portal, fixtures.contenidor_1)
        ens_1 = fixtures.create_content(contenidor_1, fixtures.ens_1)
        ens_2 = fixtures.create_content(contenidor_1, fixtures.ens_2)

        contenidor_2 = fixtures.create_content(
            self.portal, fixtures.contenidor_2)
        ens_3 = fixtures.create_content(contenidor_2, fixtures.ens_3)

        contenidor_3 = fixtures.create_content(
            self.portal, fixtures.contenidor_3)

        ens = self.reporter.list_by_contenidor_id_and_review_state(
            contenidor_1.id)
        self.assertEqual(len(ens), 2)
        self.assertEqual(ens_1.id, ens[0].id)
        self.assertEqual(ens_2.id, ens[1].id)

        ens = self.reporter.list_by_contenidor_id_and_review_state(
            contenidor_2.id)
        self.assertEqual(len(ens), 1)
        self.assertEqual(ens_3.id, ens[0].id)

        ens = self.reporter.list_by_contenidor_id_and_review_state(
            contenidor_3.id)
        self.assertEqual(len(ens), 0)

    def test_list_by_contenidor_id_and_estat_and_review_state(self):
        contenidor_1 = fixtures.create_content(
            self.portal, fixtures.contenidor_1)
        ens_1_actiu = fixtures.create_content(
            contenidor_1, fixtures.ens_1_actiu)
        ens_1_baixa = fixtures.create_content(
            contenidor_1, fixtures.ens_1_baixa)

        contenidor_2 = fixtures.create_content(
            self.portal, fixtures.contenidor_2)
        ens_2_actiu = fixtures.create_content(
            contenidor_2, fixtures.ens_2_actiu)
        ens_2_baixa = fixtures.create_content(
            contenidor_2, fixtures.ens_2_baixa)

        ens = self.reporter.list_by_contenidor_id_and_estat_and_review_state(
            contenidor_1.id, 'Actiu')
        self.assertEqual(len(ens), 1)
        self.assertEqual(ens_1_actiu.id, ens[0].id)

        ens = self.reporter.list_by_contenidor_id_and_estat_and_review_state(
            contenidor_1.id, 'Baixa')
        self.assertEqual(len(ens), 1)
        self.assertEqual(ens_1_baixa.id, ens[0].id)

        ens = self.reporter.list_by_contenidor_id_and_estat_and_review_state(
            contenidor_1.id, 'Altre')
        self.assertEqual(len(ens), 0)

        ens = self.reporter.list_by_contenidor_id_and_estat_and_review_state(
            contenidor_2.id, 'Actiu')
        self.assertEqual(len(ens), 1)
        self.assertEqual(ens_2_actiu.id, ens[0].id)

        ens = self.reporter.list_by_contenidor_id_and_estat_and_review_state(
            contenidor_2.id, 'Baixa')
        self.assertEqual(len(ens), 1)
        self.assertEqual(ens_2_baixa.id, ens[0].id)

        ens = self.reporter.list_by_contenidor_id_and_estat_and_review_state(
            contenidor_2.id, 'Altre')
        self.assertEqual(len(ens), 0)

    def test_list_by_contenidor_id_and_delta_and_review_state(self):
        contenidor_1 = fixtures.create_content(
            self.portal, fixtures.contenidor_1)
        ens_1 = fixtures.create_content(
            contenidor_1, {
                'type': 'genweb.ens.ens',
                'id': 'ens-1',
                'title': 'Ens 1',
                'acronim': 'acronim-1',
                'estat': 'estat-1',
                'effective': DateTime(2000, 1, 1, 0, 0, 0)})
        ens_2 = fixtures.create_content(
            contenidor_1, {
                'type': 'genweb.ens.ens',
                'id': 'ens-2',
                'title': 'Ens 2',
                'acronim': 'acronim-2',
                'estat': 'estat-2',
                'effective': DateTime(2000, 1, 15, 0, 0, 0)})
        ens_3 = fixtures.create_content(
            contenidor_1, {
                'type': 'genweb.ens.ens',
                'id': 'ens-3',
                'title': 'Ens 3',
                'acronim': 'acronim-3',
                'estat': 'estat-3',
                'effective': DateTime(2000, 1, 30, 0, 0, 0)})

        contenidor_2 = fixtures.create_content(
            self.portal, fixtures.contenidor_2)
        fixtures.create_content(
            contenidor_2, {
                'type': 'genweb.ens.ens',
                'id': 'ens-4',
                'title': 'Ens 4',
                'acronim': 'acronim-4',
                'estat': 'estat-4',
                'effective': DateTime(2000, 1, 15, 0, 0, 0)})

        ens = self.reporter.list_by_contenidor_id_and_delta_and_review_state(
            contenidor_1.id, -1, date_source=datetime(2000, 1, 30, 0, 0, 0))
        self.assertEqual(len(ens), 1)
        self.assertEqual(ens_3.id, ens[0].id)

        ens = self.reporter.list_by_contenidor_id_and_delta_and_review_state(
            contenidor_1.id, -15, date_source=datetime(2000, 1, 30, 0, 0, 0))
        self.assertEqual(len(ens), 2)
        self.assertEqual(ens_2.id, ens[0].id)
        self.assertEqual(ens_3.id, ens[1].id)

        ens = self.reporter.list_by_contenidor_id_and_delta_and_review_state(
            contenidor_1.id, -29, date_source=datetime(2000, 1, 30, 0, 0, 0))
        self.assertEqual(len(ens), 3)
        self.assertEqual(ens_1.id, ens[0].id)
        self.assertEqual(ens_2.id, ens[1].id)
        self.assertEqual(ens_3.id, ens[2].id)

        ens = self.reporter.list_by_contenidor_id_and_delta_and_review_state(
            contenidor_1.id, -14, date_source=datetime(2000, 1, 15, 0, 0, 0))
        self.assertEqual(len(ens), 2)
        self.assertEqual(ens_1.id, ens[0].id)
        self.assertEqual(ens_2.id, ens[1].id)

