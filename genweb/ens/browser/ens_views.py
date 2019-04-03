# -*- coding: utf-8 -*-

import json

from five import grok
from Products.CMFCore.utils import getToolByName
from plone.directives import dexterity
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.interface import Interface

from genweb.theme.browser.views import HomePageBase
from genweb.theme.browser.interfaces import IHomePageView
from genweb.ens import _
from genweb.ens.content import ens
from genweb.ens.interfaces import IGenwebEnsLayer
from genweb.ens.content.ens import IEns
from genweb.ens.content.ens import (get_percentatge_participacio,
                                    get_percentatge_membres,
                                    get_data_participacio,
                                    get_aportacio_total,
                                    get_aportacio, get_quota,
                                    get_capital_social, get_seu_social,
                                    get_observacions)
from genweb.ens.data_access.ens import EnsDataReporter
from genweb.ens.browser import helper


class View(dexterity.DisplayForm):
    grok.context(IEns)
    grok.layer(IGenwebEnsLayer)

    @property
    def percentatge_participacio(self):
        return get_percentatge_participacio(self.context)

    @property
    def percentatge_membres(self):
        return get_percentatge_membres(self.context)

    @property
    def observacions_participacio(self):
        return get_observacions(self.context, 'participacio')

    @property
    def observacions_membres(self):
        return get_observacions(self.context, 'membres')

    @property
    def observacions_quota(self):
        return get_observacions(self.context, 'quota')

    @property
    def data_participacio(self):
        return get_data_participacio(self.context)

    @property
    def aportacio_total(self):
        return get_aportacio_total(self.context)

    @property
    def aportacio(self):
        return get_aportacio(self.context)

    @property
    def quota(self):
        return get_quota(self.context)

    @property
    def capital_social(self):
        return get_capital_social(self.context)

    @property
    def seu_social(self):
        return get_seu_social(self.context)

    @property
    def adscripcio(self):
        return self.context.adscripcio or "-"

    @property
    def unitats(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_unitats_by_ens_obj(self.context)

    @property
    def acords(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_acords_by_ens_obj(self.context)

    @property
    def estatuts_vigents(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_estatuts_by_ens_obj(self.context, is_vigent=True)

    @property
    def estatuts_historics(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_estatuts_by_ens_obj(self.context, is_vigent=False)

    @property
    def escriptures(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_escriptures_by_ens_obj(self.context)

    @property
    def documents_interes(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_documents_interes_by_ens_obj(self.context)

    @property
    def convenis(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_convenis_by_ens_obj(self.context)

    @property
    def actes_reunio(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_actes_reunio_by_ens_obj(self.context)

    @property
    def organs_govern(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_organs_by_ens(self.context, tipus="Govern")

    @property
    def organs_assessors(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_organs_by_ens(self.context, tipus="Assessor")

    @property
    def directius(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_directius_by_ens_obj(self.context)

    @property
    def contactes(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_contactes_by_ens_obj(self.context)

    def get_file_href(self, content):
        return "{0}/view/++widget++form.widgets.fitxer/@@download/{1}".format(
            content.absolute_url(), content.fitxer.filename.encode('utf-8'))

    def list_carrecs_by_organ(self, organ, is_historic=None):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_carrecs_by_organ_grouped_by_ens_obj(
            organ, is_historic=is_historic)

    def prettify_organ_title(self, organ):
        return "{0}{1}".format(
            organ.Title,
            _(u" (Històric)").encode('utf-8') if organ.is_historic else u"")

    def getData(self):
        ens = self.context
        if ens.estat == 'Actiu':
            data = ens.data_entrada.strftime('%d/%m/%Y') if ens.data_entrada else '-'
        elif ens.estat == 'Baixa':
            data = ens.data_baixa.strftime('%d/%m/%Y') if ens.data_baixa else '-'
        else:
            data = '-'
        return data


class Search(HomePageBase):
    grok.name('homepage')
    grok.implements(IHomePageView)
    grok.context(INavigationRoot)
    grok.layer(IGenwebEnsLayer)

    @property
    def figura_juridica_vocabulary(self):
        return [('', _(u"Qualsevol"))] + [
            (value, value) for value in ens.figura_juridica_values]

    @property
    def estat_vocabulary(self):
        return [('', _(u"Qualsevol"))] + [
            (value, value) for value in ens.estat_values]

    @property
    def carpetes_vocabulary(self):
        return helper.get_carpetes_vocabulary(self)


class SearchResults(grok.View):
    grok.context(Interface)
    grok.name('ens_search_results')
    grok.layer(IGenwebEnsLayer)

    def parse_search_filters(self):
        search_filters = {}

        figura_juridica = self.request.form.get('figura_juridica', '')
        if figura_juridica:
            search_filters['figura_juridica'] = figura_juridica.decode('utf-8')

        estat = self.request.form.get('estat', '')
        if estat:
            search_filters['estat'] = estat.decode('utf-8')

        try:
            carpetes = json.loads(self.request.form.get('carpetes', ''))
            if carpetes:
                search_filters["path"] = {"depth": 1}
                search_filters["path"]["query"] = carpetes
        except ValueError:
            pass

        text = self.request.form.get('text', None)
        if text:
            search_filters['SearchableText'] = "*{0}*".format(text)

        return search_filters

    def search(self):
        reporter = EnsDataReporter(
            getToolByName(self.context, 'portal_catalog'))
        return reporter.search(self.parse_search_filters())
