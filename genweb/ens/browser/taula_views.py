# -*- coding: utf-8 -*-

from StringIO import StringIO
import csv

from five import grok
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName

from genweb.ens.interfaces import IGenwebEnsLayer
from genweb.ens.data_access.ens import EnsDataReporter


class TaulaIdentificativa(grok.View):
    grok.name('taula_identificativa')
    grok.context(Interface)
    grok.template('taula_identificativa')
    grok.layer(IGenwebEnsLayer)

    def list(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_identificacio()


class TaulaIdentificativaCsv(grok.View):
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
        writer = csv.writer(output_file)
        writer.writerow(TaulaIdentificativaCsv.data_header_columns)
        for ens in reporter.list_identificacio():
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


class TaulaRepresentacio(grok.View):
    grok.name('taula_representacio')
    grok.context(Interface)
    grok.template('taula_representacio')
    grok.layer(IGenwebEnsLayer)

    def list(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_representacio()


class TaulaRepresentacioCsv(grok.View):
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
        writer = csv.writer(output_file)
        writer.writerow(TaulaRepresentacioCsv.data_header_columns)
        for ens in reporter.list_representacio(is_historic=False):
            writer.writerow([
                ens.denominacio.encode('utf-8'),
                ens.organ.encode('utf-8'),
                ens.persona.encode('utf-8'),
                ens.carrec.encode('utf-8'),
                ens.data_nomenament.encode('utf-8')
            ])
