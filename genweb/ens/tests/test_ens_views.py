# -*- coding: utf-8 -*-

"""Functional tests for ens views."""

from plone.testing.z2 import Browser
from transaction import commit

from genweb.ens.testing import FunctionalTestCase
from genweb.ens.tests.fixtures import fixtures


class TestEnsViews(FunctionalTestCase):
    """Test taula views functions."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.browser = Browser(self.layer['portal'])

    def assertAppearsBefore(self, subtxt_1, subtxt_2, txt):
        self.assertIn(subtxt_1, txt)
        self.assertIn(subtxt_2, txt)
        self.assertTrue(txt.find(subtxt_1) < txt.find(subtxt_2))

    def assertAppearInOrder(self, subtxts, txt):
        def assertAppearsBefore(subtxt_1, subtxt_2):
            self.assertAppearsBefore(subtxt_1, subtxt_2, txt)
            return subtxt_2
        reduce(assertAppearsBefore, subtxts)

    def test_view_displays_all_fields_in_order(self):
        ens = fixtures.create_content(self.layer['portal'], fixtures.ens_ai)
        directiu_1 = fixtures.create_content(ens, fixtures.persona_directiu_1)
        directiu_2 = fixtures.create_content(ens, fixtures.persona_directiu_2)
        contacte_1 = fixtures.create_content(ens, fixtures.persona_contacte_1)
        contacte_2 = fixtures.create_content(ens, fixtures.persona_contacte_2)
        organ_2 = fixtures.create_content(ens, fixtures.organ_2)
        organ_3 = fixtures.create_content(ens, fixtures.organ_3)
        organ_1 = fixtures.create_content(ens, fixtures.organ_1)
        organ_5 = fixtures.create_content(ens, fixtures.organ_5)
        organ_4 = fixtures.create_content(ens, fixtures.organ_4)
        organ_6 = fixtures.create_content(ens, fixtures.organ_6)
        carrec_1 = fixtures.create_content(organ_1, fixtures.carrec_1)
        carrec_2 = fixtures.create_content(organ_1, fixtures.carrec_2)
        carrec_3 = fixtures.create_content(organ_1, fixtures.carrec_3)
        carrec_4 = fixtures.create_content(organ_1, fixtures.carrec_4)
        carrec_5 = fixtures.create_content(organ_1, fixtures.carrec_5)
        unitat_1 = fixtures.create_content(ens, fixtures.unitat_1)
        unitat_2 = fixtures.create_content(ens, fixtures.unitat_2)
        acord_1 = fixtures.create_content(ens, fixtures.acord_1)
        acord_2 = fixtures.create_content(ens, fixtures.acord_2)
        acord_3 = fixtures.create_content(ens, fixtures.acord_3)
        acord_4 = fixtures.create_content(ens, fixtures.acord_4)
        escriptura_1 = fixtures.create_content(ens, fixtures.escriptura_1)
        escriptura_2 = fixtures.create_content(ens, fixtures.escriptura_2)
        escriptura_3 = fixtures.create_content(ens, fixtures.escriptura_3)
        escriptura_4 = fixtures.create_content(ens, fixtures.escriptura_4)
        estatut_1 = fixtures.create_content(ens, fixtures.estatut_1)
        estatut_2 = fixtures.create_content(ens, fixtures.estatut_2)
        estatut_3 = fixtures.create_content(ens, fixtures.estatut_3)
        estatut_4 = fixtures.create_content(ens, fixtures.estatut_4)
        estatut_5 = fixtures.create_content(ens, fixtures.estatut_5)
        estatut_6 = fixtures.create_content(ens, fixtures.estatut_6)
        acta_1 = fixtures.create_content(ens, fixtures.acta_1)
        acta_2 = fixtures.create_content(ens, fixtures.acta_2)
        acta_3 = fixtures.create_content(ens, fixtures.acta_3)
        conveni_1 = fixtures.create_content(ens, fixtures.conveni_1)
        conveni_2 = fixtures.create_content(ens, fixtures.conveni_2)
        conveni_3 = fixtures.create_content(ens, fixtures.conveni_3)
        document_1 = fixtures.create_content(ens, fixtures.document_1)
        document_2 = fixtures.create_content(ens, fixtures.document_2)
        document_3 = fixtures.create_content(ens, fixtures.document_3)
        commit()

        self.browser.open(ens.absolute_url())

        self.assertAppearInOrder([
            "<dt>Denominació</dt>",
            "<dd>{0}</dd>".format(ens.title.encode('utf-8')),
            "<dt>Acrònim</dt>",
            "<dd>{0}</dd>".format(ens.acronim.encode('utf-8')),
            "<dt>Descripció</dt>",
            '<dd class="fieldset-end">{0}</dd>'.format(
                ens.description.encode('utf-8')),
            "<dt>Estat</dt>",
            "<dd>{0}</dd>".format(ens.estat.encode('utf-8')),
            "<dt>NIF</dt>",
            "<dd>{0}</dd>".format(ens.nif.encode('utf-8')),
            '<dt>Figura jurídica</dt>',
            "<dd>{0}</dd>".format(
                ens.figura_juridica.encode('utf-8')),
            '<dt class="subfield">Núm. Identif.</dt>',
            '<dd class="fieldset-end">{0}</dd>'.format(
                ens.numero_identificacio.encode('utf-8')),
            "<dt>Domicili social</dt>",
            "<dd>{0}</dd>".format(ens.domicili_social.encode('utf-8')),
            "<dt>Adreça oficines 1</dt>",
            "<dd>{0}</dd>".format(ens.adreca_oficines_1.encode('utf-8')),
            "<dt>Adreça oficines 2</dt>",
            "<dd>{0}</dd>".format(ens.adreca_oficines_2.encode('utf-8')),
            "<dt>Telèfon</dt>",
            "<dd>{0}</dd>".format(ens.telefon.encode('utf-8')),
            "<dt>Fax</dt>",
            "<dd>{0}</dd>".format(ens.fax.encode('utf-8')),
            "<dt>Web</dt>",
            '<dd class="fieldset-end">{0}</dd>'.format(
                ens.web.encode('utf-8')),
            "<dt>Tipologia UPC</dt>",
            "<dd>{0}</dd>".format(ens.tipologia_upc.encode('utf-8')),
            "<dt>Codi UPC</dt>",
            '<dd class="fieldset-end">{0}</dd>'.format(
                ens.codi.encode('utf-8')),
            "<dt>Observacions</dt>",
            "<dd>{0}</dd>".format(
                ens.dades_identificatives_observacions.encode('utf-8')),
            ], self.browser.contents)

        self.assertIn("<h3>Càrrecs directius</h3>", self.browser.contents)

        for directiu in (directiu_1, directiu_2):
            self.assertIn(directiu.title.encode('utf-8'),
                          self.browser.contents)
            self.assertIn(directiu.carrec.encode('utf-8'),
                          self.browser.contents)
            self.assertIn(directiu.telefon.encode('utf-8'),
                          self.browser.contents)
            self.assertIn(directiu.email.encode('utf-8'),
                          self.browser.contents)

        self.assertIn("<h3>Persones de contacte</h3>", self.browser.contents)

        for contacte in (contacte_1, contacte_2):
            self.assertIn(contacte.title.encode('utf-8'),
                          self.browser.contents)
            self.assertIn(contacte.carrec.encode('utf-8'),
                          self.browser.contents)
            self.assertIn(contacte.telefon.encode('utf-8'),
                          self.browser.contents)
            self.assertIn(contacte.email.encode('utf-8'),
                          self.browser.contents)

        self.assertIn("<dt>Aportació inicial</dt>", self.browser.contents)
        self.assertIn("<dd>2,300.50 €/any</dd>", self.browser.contents)

        self.assertIn("<dt>Quota</dt>", self.browser.contents)
        self.assertIn("<dd>253.44 €/mes</dd>", self.browser.contents)

        self.assertIn("<dt>Unitat de càrrec</dt>", self.browser.contents)
        self.assertIn("<dd>{0}</dd>".format(ens.unitat_carrec.encode('utf-8')),
                      self.browser.contents)

        self.assertIn("<dt>Percentatge de participació</dt>",
                      self.browser.contents)
        self.assertIn("<dd>15.35%</dd>", self.browser.contents)

        self.assertIn("<dt>Nombre de membres UPC</dt>", self.browser.contents)
        self.assertIn("<dd>{0}</dd>".format(
            ens.nombre_membres.encode('utf-8')),
            self.browser.contents)

        self.assertIn("<dt>Part. en cap. social o fons patrimonial</dt>",
                      self.browser.contents)
        self.assertIn("<dd>2,000.00 EUR</dd>", self.browser.contents)

        self.assertIn("<dt>Observacions</dt>", self.browser.contents)
        self.assertIn("<dd>{0}</dd>".format(
            ens.participacio_observacions.encode('utf-8')),
            self.browser.contents)

        self.assertAppearInOrder([
            organ_2.title.encode('utf-8'),
            organ_3.title.encode('utf-8'),
            organ_1.title.encode('utf-8'),
            organ_5.title.encode('utf-8'),
            organ_4.title.encode('utf-8'),
            organ_6.title.encode('utf-8')],
            self.browser.contents)

        self.assertAppearsBefore(
            "<h3>Òrgans de govern</h3>",
            organ_1.title.encode('utf-8'),
            self.browser.contents)

        self.assertAppearInOrder([
            carrec_1.title.encode('utf-8'),
            carrec_2.title.encode('utf-8'),
            carrec_4.title.encode('utf-8'),
            carrec_3.title.encode('utf-8'),
            carrec_5.title.encode('utf-8')],
            self.browser.contents)

        self.assertAppearsBefore(
            "<h3>Òrgans assessors</h3>",
            organ_4.title.encode('utf-8'),
            self.browser.contents)

        self.assertAppearInOrder([
            "<h3>Unitats UPC implicades</h3>",
            unitat_2.title.encode('utf-8'),
            unitat_1.title.encode('utf-8')],
            self.browser.contents)

        self.assertIn("<dt>Data de constitució</dt>", self.browser.contents)
        self.assertIn("<dd>17/02/2005</dd>", self.browser.contents)

        self.assertIn("<dt>Entitats constituents</dt>", self.browser.contents)
        self.assertIn("<dd>{0}</dd>".format(
            ens.entitats_constituents.encode('utf-8')), self.browser.contents)

        self.assertIn("<dt>Entitats actuals</dt>", self.browser.contents)
        self.assertIn("<dd>{0}</dd>".format(
            ens.entitats_actuals.encode('utf-8')), self.browser.contents)

        self.assertIn("<dt>Data d&apos;entrada UPC</dt>",
                      self.browser.contents)
        self.assertIn("<dd>11/03/2015</dd>", self.browser.contents)

        self.assertIn('<dt class="subfield">Descripció</dt>',
                      self.browser.contents)
        self.assertIn("<dd>{0}</dd>".format(
            ens.data_entrada_descripcio.encode('utf-8')),
            self.browser.contents)

        self.assertIn("<dt>Seu social</dt>", self.browser.contents)
        self.assertIn("<dd>{0}</dd>".format(
            ens.seu_social.encode('utf-8')), self.browser.contents)

        self.assertIn("<dt>Observacions</dt>", self.browser.contents)
        self.assertIn("<dd>{0}</dd>".format(
            ens.marc_legal_observacions.encode('utf-8')),
            self.browser.contents)

        self.assertAppearInOrder([
            "<h3>Acords òrgans de govern</h3>",
            acord_1.title.encode('utf-8'),
            acord_4.title.encode('utf-8'),
            acord_2.title.encode('utf-8'),
            acord_3.title.encode('utf-8')],
            self.browser.contents)

        self.assertAppearInOrder([
            "<h3>Escriptures públiques</h3>",
            escriptura_4.title.encode('utf-8'),
            escriptura_1.title.encode('utf-8'),
            escriptura_2.title.encode('utf-8'),
            escriptura_3.title.encode('utf-8')],
            self.browser.contents)

        self.assertAppearInOrder([
            "<h3>Estatuts</h3>",
            "<h4>Vigents</h4>",
            estatut_2.title.encode('utf-8'),
            estatut_3.title.encode('utf-8'),
            estatut_1.title.encode('utf-8'),
            "<h4>Anteriors</h4>",
            estatut_4.title.encode('utf-8'),
            estatut_6.title.encode('utf-8'),
            estatut_5.title.encode('utf-8')],
            self.browser.contents)

        self.assertAppearInOrder([
            "<h3>Actes de reunions</h3>",
            acta_2.title.encode('utf-8'),
            acta_1.title.encode('utf-8'),
            acta_3.title.encode('utf-8')],
            self.browser.contents)

        self.assertAppearInOrder([
            "<h3>Convenis</h3>",
            conveni_3.title.encode('utf-8'),
            conveni_1.title.encode('utf-8'),
            conveni_2.title.encode('utf-8')],
            self.browser.contents)

        self.assertAppearInOrder([
            "<h3>Altres documents d&apos;interès</h3>",
            document_2.title.encode('utf-8'),
            document_3.title.encode('utf-8'),
            document_1.title.encode('utf-8')],
            self.browser.contents)
