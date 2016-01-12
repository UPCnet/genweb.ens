# -*- coding: utf-8 -*-
"""Integration tests for taula views."""
import os
from StringIO import StringIO
from datetime import datetime

from plone import api

from genweb.ens.testing import IntegrationTestCase


class TestTaulaViews(IntegrationTestCase):
    """Test taula views functions."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.folder_files_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'files')

    def test_taula_identificativa_csv_write_data(self):
        api.content.create(
            container=self.layer['portal'],
            type='genweb.ens.ens',
            id='amnistia-internacional',
            title=u"Amnistía Internacional",
            acronim=u"AI",
            codi=u"11A",
            nif=u"X82771235",
            estat=u"Pre-alta cancel·lada",
            figura_juridica=u"Fundació",
            seu_social=u"Resta d'Espanya",
            seu_social_stranger=None,
            percentatge_participacio=15.35,
            aportacio_sn=True,
            aportacio_import=2300.50,
            aportacio_moneda=u"€/any",
            quota_sn=True,
            quota_import=253.44,
            quota_moneda=u"€/mes",
            web=u"www.amnistia.org")

        api.content.create(
            container=self.layer['portal'],
            type='genweb.ens.ens',
            id='amitges',
            title=u"Amitges",
            acronim=u"Amt")

        api.content.create(
            container=self.layer['portal'],
            type='genweb.ens.ens',
            id='green peace',
            title=u"Green Peace",
            acronim=u"Gp",
            codi=u"22A",
            nif=None,
            estat=u"Pre-Baixa",
            figura_juridica=u"Sense NIF",
            seu_social=u"Estranger",
            seu_social_estranger=u"Dublín",
            percentatge_participacio=None,
            aportacio_sn=False,
            aportacio_import=None,
            aportacio_moneda=None,
            quota_sn=True,
            quota_import=253.44,
            quota_moneda=None,
            web=u"www.greenpeace.org")

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
        ens = api.content.create(
            container=self.layer['portal'],
            type='genweb.ens.ens',
            id='amnistia-internacional',
            title=u"Amnistía Internacional",
            acronim=u"AI",
            codi=u"11A",
            nif=u"X82771235",
            estat=u"Pre-alta cancel·lada",
            figura_juridica=u"Fundació",
            seu_social=u"Resta d'Espanya",
            seu_social_stranger=None,
            percentatge_participacio=15.35,
            aportacio_sn=True,
            aportacio_import=2300.50,
            aportacio_moneda=u"€/any",
            quota_sn=True,
            quota_import=253.44,
            quota_moneda=u"€/mes",
            web=u"www.amnistia.org")

        organ = api.content.create(
            container=ens,
            type='genweb.ens.organ',
            id='consell-de-direccio',
            title=u'Consell de Direcció',
            tipus='Govern')

        api.content.create(
            container=organ,
            type='genweb.ens.carrec_upc',
            id='colomina-pardo-otto',
            title=u'Colomina Pardo, Ottö',
            carrec=u"Membre excel·lent",
            is_historic=False,
            data_inici=datetime(2015, 2, 15))

        api.content.create(
            container=self.layer['portal'],
            type='genweb.ens.ens',
            id='green peace',
            title=u"Green Peace",
            acronim=u"Gp",
            codi=u"22A",
            nif=None,
            estat=u"Pre-Baixa",
            figura_juridica=u"Sense NIF",
            seu_social=u"Estranger",
            seu_social_estranger=u"Dublín",
            percentatge_participacio=None,
            aportacio_sn=False,
            aportacio_import=None,
            aportacio_moneda=None,
            quota_sn=True,
            quota_import=253.44,
            quota_moneda=None,
            web=u"www.greenpeace.org")

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
