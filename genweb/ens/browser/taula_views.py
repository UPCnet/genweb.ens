# -*- coding: utf-8 -*-

from StringIO import StringIO
import json
import csv

from five import grok
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName

from genweb.ens.interfaces import IGenwebEnsLayer
from genweb.ens.data_access.ens import EnsDataReporter


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


class TaulaIdentificativa(grok.View, Taula):
    grok.name('taula_identificativa')
    grok.context(Interface)
    grok.layer(IGenwebEnsLayer)

    def list(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_identificacio(self.parse_search_filters())

    @property
    def export_url(self):
        query_string = 'carpetes=' + self.request.form.get('carpetes', '')
        return '{0}/taula_identificativa_csv?{1}'.format(
            self.context.absolute_url(), query_string)


class TaulaIdentificativaCsv(grok.View, Taula):
    grok.name('taula_identificativa_csv')
    grok.context(Interface)
    grok.layer(IGenwebEnsLayer)

    data_header_columns = [
        "Codi",
        "Denominació",
        "NIF",
        "Estat",
        "Fig. jurídica",
        "Seu social",
        "% part.",
        "Ap. inicial",
        "Quota",
        "Web"]

    def render(self):
        output_file = StringIO()
        # Write the BOM of the text stream to make its charset explicit
        output_file.write(u'\ufeff'.encode('utf8'))
        self.write_data(output_file)

        header_content_type = 'text/csv'
        header_filename = 'taula_identificativa.csv'
        self.request.response.setHeader('Content-Type', header_content_type)
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="{0}"'.format(header_filename))
        return output_file.getvalue()

    def write_data(self, output_file):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        writer = csv.writer(output_file, dialect='excel', delimiter=';')
        writer.writerow(TaulaIdentificativaCsv.data_header_columns)

        for ens in reporter.list_identificacio(self.parse_search_filters()):
            writer.writerow([
                ens.codi.encode('utf-8'),
                ens.denominacio.encode('utf-8'),
                ens.nif.encode('utf-8'),
                ens.estat.encode('utf-8'),
                ens.figura_juridica.encode('utf-8'),
                ens.seu_social.encode('utf-8'),
                ens.percentatge_participacio.encode('utf-8'),
                ens.aportacio.encode('utf-8'),
                ens.quota.encode('utf-8'),
                ens.web.encode('utf-8')
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
        "Òrgan",
        "Persona",
        "Càrrec",
        "Data nom."]

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
                ens.denominacio.encode('utf-8'),
                ens.organ.encode('utf-8'),
                ens.persona.encode('utf-8'),
                ens.carrec.encode('utf-8'),
                ens.data_nomenament.encode('utf-8')
            ])


class TaulaTransparencia(grok.View, Taula):
    grok.name('taula_transparencia')
    grok.context(Interface)
    grok.layer(IGenwebEnsLayer)
