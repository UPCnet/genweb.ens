# -*- coding: utf-8 -*-

from StringIO import StringIO
import json
import csv

from plone import api

from five import grok
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName

from genweb.ens.interfaces import IGenwebEnsLayer
from genweb.ens.data_access.ens import EnsDataReporter
from Products.PythonScripts.standard import url_quote


class Taula(object):
    def parse_search_filters(self):
        search_filters = {}
        try:
            carpetes = json.loads(self.request.form.get('carpetes', ''))
            if carpetes:
                search_filters["path"] = {"depth": 1}
                search_filters["path"]["query"] = [
                    carpeta for carpeta in carpetes]
        except ValueError:
            pass
        return search_filters


class TauladEntitats(grok.View, Taula):
    grok.name('taula_dentitats')
    grok.context(Interface)
    grok.layer(IGenwebEnsLayer)

    def list(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_entitats(self.parse_search_filters())

    @property
    def export_url(self):
        query_string = 'carpetes=' + self.request.form.get('carpetes', '')
        return '{0}/taula_dentitats_csv?{1}'.format(
            self.context.absolute_url(), query_string)

    def getSeu(self, ens):
        if 'Estranger' in ens.seu_social:
            seu = ens.seu_social + ' (' + ens.seu_social_estranger + ')'
        else:
            seu = ens.seu_social
        return seu

    def getTags(self, ens):
        tags = []
        lang = api.portal.get_current_language()
        portal_url = api.portal.get().absolute_url() + '/' + lang
        categories = ens.tags
        try:
            for category in categories():
                quotedCat = url_quote(category)
                tag_link = portal_url + '/@@search?Subject%3Alist=' + quotedCat
                tag = {'tag_name': category, 'tag_url': tag_link}
                tags.append(tag)
            return tags
        except:
            return []


class TauladEntitatsCsv(grok.View, Taula):
    grok.name('taula_dentitats_csv')
    grok.context(Interface)
    grok.layer(IGenwebEnsLayer)

    data_header_columns = [
        "Denominació",
        "Acrònim",
        "Estat",
        "NIF",
        "Àmbit institucional",
        "Figura jurídica",
        "Identificadors",
        "Web",
        "Tipologia UPC",
        "Codi UPC",
        "Núm. UPC",
        "Etiquetes",
        "Data alta UPC",
        "Data baixa UPC",
        "Fons patrimonial (data)",
        "Cap. inicial total",
        "Aportació inicial UPC",
        "% UPC en capital",
        "% UPC en vots",
        "Quota",
        "Entitats constituents",
        "Entitats actuals",
        "Data de constitució",
        "Data alta UPC",
        "Acord UPC",
        "Adscripció",
        "Data estatuts"]

    def render(self):
        output_file = StringIO()
        # Write the BOM of the text stream to make its charset explicit
        output_file.write(u'\ufeff'.encode('utf8'))
        self.write_data(output_file)

        header_content_type = 'text/csv'
        header_filename = 'taula_d\'entitats.csv'
        self.request.response.setHeader('Content-Type', header_content_type)
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="{0}"'.format(header_filename))
        return output_file.getvalue()

    def write_data(self, output_file):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        writer = csv.writer(output_file, dialect='excel', delimiter=';')
        writer.writerow(TauladEntitatsCsv.data_header_columns)

        for ens in reporter.list_entitats(self.parse_search_filters()):
            ens_tags = ",".join([str(tag) for tag in ens.tags()])
            if ens.entitats_constituents and ens.entitats_constituents != '-':
                pass

            writer.writerow([
                ens.title.encode('utf-8') or "-",
                ens.acronim.encode('utf-8') or "-",
                ens.estat.encode('utf-8') or "-",
                ens.nif.encode('utf-8') or "-",
                ens.institution_type.encode('utf-8') or "-",
                ens.figura_juridica.encode('utf-8') or "-",
                ens.numero_identificacio or "-",
                ens.web.encode('utf-8') or "-",
                ens.tipologia_upc.encode('utf-8') or "-",
                ens.codi.encode('utf-8') or "-",
                ens.num_ens or "-",
                ens_tags or "-",
                ens.data_entrada or "-",
                ens.data_baixa or "-",
                ens.capital_social.encode('utf-8') or "-",
                ens.aportacio_total.encode('utf-8') or "-",
                ens.aportacio_import.encode('utf-8') or "-",
                ens.percentatge_participacio.encode('utf-8') or "-",
                ens.percentatge_membres.encode('utf-8') or "-",
                ens.quota.encode('utf-8') or "-",
                ens.entitats_constituents.encode('utf-8') or "-",
                ens.entitats_actuals.encode('utf-8') or "-",
                ens.data_constitucio or "-",
                ens.data_entrada or "-",
                ens.data_entrada_acord.encode('utf-8') or "-",
                ens.adscripcio.encode('utf-8') or "-",
                ens.data_estatuts.encode('utf-8') or "-"
            ])


class TaulaRepresentacio(grok.View, Taula):
    grok.name('taula_representacio')
    grok.context(Interface)
    grok.layer(IGenwebEnsLayer)

    def list(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_representacio(
            is_historic=False,
            search_filters=self.parse_search_filters())

    @property
    def export_url(self):
        query_string = 'carpetes=' + self.request.form.get('carpetes', '')
        return '{0}/taula_representacio_csv?{1}'.format(
            self.context.absolute_url(), query_string)


class TaulaRepresentacioCsv(grok.View, Taula):
    grok.name('taula_representacio_csv')
    grok.context(Interface)
    grok.layer(IGenwebEnsLayer)

    data_header_columns = [
        "Denominació",
        "Acrònim",
        "Òrgan",
        "Càrrec a l'òrgan",
        "Nom persona",
        "En qualitat de ...",
        "Data inici",
        "Vigència",
        "Data fi"]

    def render(self):
        output_file = StringIO()
        # Write the BOM of the text stream to make its charset explicit
        output_file.write(u'\ufeff'.encode('utf8'))
        self.write_data(output_file)

        header_content_type = 'text/csv'
        header_filename = 'taula_representacio.csv'
        self.request.response.setHeader('Content-Type', header_content_type)
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="{0}"'.format(header_filename))
        return output_file.getvalue()

    def write_data(self, output_file):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        writer = csv.writer(output_file, dialect='excel', delimiter=';')
        writer.writerow(TaulaRepresentacioCsv.data_header_columns)

        for ens in reporter.list_representacio(
                is_historic=False,
                search_filters=self.parse_search_filters()):
            writer.writerow([
                ens.denominacio.encode('utf-8') or "-",
                ens.acronim.encode('utf-8') or "-",
                ens.organ.encode('utf-8') or "-",
                ens.carrec.encode('utf-8') or "-",
                ens.persona.encode('utf-8') or "-",
                ens.qualitat.encode('utf-8') or "-",
                ens.data_inici or "-",
                ens.vigencia or "-",
                ens.data_fi or "-",
            ])
