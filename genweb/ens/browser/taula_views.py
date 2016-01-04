# -*- coding: utf-8 -*-

from StringIO import StringIO
import csv

from five import grok
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName

from genweb.ens.interfaces import IGenwebEnsLayer
from genweb.ens.content.ens import (get_percentatge_participacio,
                                    get_quota, get_aportacio, get_seu_social)


class TaulaIdentificativa(grok.View):
    grok.name('taula_identificativa')
    grok.context(Interface)
    grok.template('taula_identificativa')
    grok.layer(IGenwebEnsLayer)

    def list_ens_obj(self):
        catalog = getToolByName(self, 'portal_catalog')

        return [ens.getObject() for ens in catalog.searchResults(
            portal_type='genweb.ens.ens',
            sort_on='sortable_title',
            )]

    def prettify_percentatge_participacio(self, ens):
        return get_percentatge_participacio(ens)

    def prettify_quota(self, ens):
        return get_quota(ens)

    def prettify_aportacio(self, ens):
        return get_aportacio(ens)

    def prettify_seu_social(self, ens):
        return get_seu_social(ens)


class TaulaIdentificativaCsv(grok.View):
    grok.name('taula_identificativa_csv')
    grok.context(Interface)
    grok.layer(IGenwebEnsLayer)

    def render(self):
        output_file = StringIO()
        self.write_data(output_file)

        header_content_type = 'text/csv'
        header_filename = "taula_identificativa.csv"
        self.request.response.setHeader('Content-Type', header_content_type)
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="{0}"'.format(header_filename))
        return output_file.getvalue()

    def write_data(self, output_file):
        writer = csv.writer(output_file)
        writer.writerow([
            "acrònim",
            "denom. comp.",
            "nif",
            "estat",
            "fig. jurídica",
            "seu social",
            "% part.",
            "ap. inicial",
            "quota",
            "web"
            ])

        catalog = getToolByName(self, 'portal_catalog')
        for ens in catalog.searchResults(
                portal_type='genweb.ens.ens',
                sort_on='sortable_title'):
            ens_obj = ens.getObject()
            writer.writerow([
                ens_obj.acronim and ens_obj.acronim.encode('utf-8'),
                ens_obj.title and ens_obj.title.encode('utf-8'),
                ens_obj.nif and ens_obj.nif.encode('utf-8'),
                ens_obj.estat and ens_obj.estat.encode('utf-8'),
                ens_obj.figura_juridica and ens_obj.figura_juridica.encode(
                    'utf-8'),
                get_seu_social(ens_obj).encode('utf-8'),
                get_percentatge_participacio(ens_obj).encode('utf-8'),
                get_aportacio(ens_obj).encode('utf-8'),
                get_quota(ens_obj).encode('utf-8'),
                ens_obj.web and ens_obj.web.encode('utf-8')
            ])


class TaulaRepresentacio(grok.View):
    grok.name('taula_representacio')
    grok.context(Interface)
    grok.template('taula_representacio')
    grok.layer(IGenwebEnsLayer)
