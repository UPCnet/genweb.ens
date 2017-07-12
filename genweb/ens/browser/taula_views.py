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
                tag_link =  portal_url + '/@@search?Subject%3Alist=' + quotedCat
                tag = {'tag_name': category,'tag_url': tag_link}
                tags.append(tag)
            return tags
        except:
            return []


class TaulaIdentificativaCsv(grok.View, Taula):
    grok.name('taula_identificativa_csv')
    grok.context(Interface)
    grok.layer(IGenwebEnsLayer)

    data_header_columns = [
        "Codi REP",
        "Acrònim",
        "Denominació",
        "NIF",
        "Num. Identificacio",
        "Estat",
        "Fig. jurídica",
        "Tipus institució",
        "Tipologia UPC",
        "Seu social",
        "Adm. Púb. Adscrip.",
        "Participació",
        "Membres UPC",
        "Quota",
        "Etiquetes",
        "Etiquetes antigues",
        "Web",
        "Entitats participants"]

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
            ens_tags = ",".join([str(tag) for tag in ens.tags()])
            writer.writerow([
                ens.codi.encode('utf-8'),
                ens.acronim.encode('utf-8'),
                ens.title.encode('utf-8'),
                ens.nif.encode('utf-8'),
                ens.numero_identificacio.encode('utf-8'),
                ens.estat.encode('utf-8'),
                ens.figura_juridica.encode('utf-8'),
                ens.institution_type.encode('utf-8'),
                ens.tipologia_upc.encode('utf-8'),
                ens.seu_social.encode('utf-8'),
                ens.adscripcio.encode('utf-8'),
                ens.percentatge_participacio.encode('utf-8'),
                ens.nombre_membres.encode('utf-8'),
                ens.quota.encode('utf-8'),
                ens_tags,
                ens.etiquetes.encode('utf-8'),
                ens.web.encode('utf-8'),
                ens.entitats_actuals.encode('utf-8')                
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
        "Càrrec"
        "Persona",
        "Com a...",
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
                ens.carrec.encode('utf-8'),
                ens.persona.encode('utf-8'),
                ens.carrec_envirtud.encode('utf-8'),
                ens.data_nomenament.encode('utf-8')
            ])
