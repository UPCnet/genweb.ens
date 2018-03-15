# -*- coding: utf-8 -*-

from StringIO import StringIO
import json
import csv

from plone import api
from five import grok
from zope.interface import Interface

from genweb.ens.interfaces import IGenwebEnsLayer


def getRepresentantsUPC():
    catalog = api.portal.get_tool('portal_catalog')
    root_path = '/'.join(api.portal.get().getPhysicalPath())
    language = api.portal.get_current_language()
    path = root_path + '/' + language + '/representants-upc/altres'
    return catalog(portal_type=('genweb.ens.representant'),
                   path=path)


class TaulaRepresentatsUpc(grok.View):
    grok.name('taula_representants_upc')
    grok.context(Interface)
    grok.layer(IGenwebEnsLayer)
    grok.require('genweb.authenticated')
    grok.template('taularepresentantsupc')

    def list(self):
        return getRepresentantsUPC()

    @property
    def export_url(self):
        return '{0}/taula_representants_upc_csv'.format(self.context.absolute_url())


class TaulaRepresentatsUpcCsv(grok.View):
    grok.name('taula_representants_upc_csv')
    grok.context(Interface)
    grok.layer(IGenwebEnsLayer)
    grok.require('genweb.authenticated')

    data_header_columns = [
        "Representant",
        "DNI",
        "Col·lectiu"]

    def render(self):
        output_file = StringIO()
        # Write the BOM of the text stream to make its charset explicit
        output_file.write(u'\ufeff'.encode('utf8'))
        self.write_data(output_file)

        header_content_type = 'text/csv'
        header_filename = 'taula_representants_upc.csv'
        self.request.response.setHeader('Content-Type', header_content_type)
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="{0}"'.format(header_filename))
        return output_file.getvalue()


    def list(self):
        return getRepresentantsUPC()

    def write_data(self, output_file):
        writer = csv.writer(output_file, dialect='excel', delimiter=';')
        writer.writerow(TaulaRepresentatsUpcCsv.data_header_columns)

        for representant in self.list():
            representant = representant.getObject()

            if representant.dni == None:
                representant.dni = ''
            if representant.carrec == None:
                representant.carrec = ''

            writer.writerow([
                representant.title.encode('utf-8'),
                representant.dni.encode('utf-8'),
                representant.carrec.encode('utf-8')
            ])
