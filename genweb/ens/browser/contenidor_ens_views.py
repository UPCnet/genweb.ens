# -*- coding: utf-8 -*-

import json

from five import grok
from Products.CMFCore.utils import getToolByName

from genweb.ens import _
from genweb.ens.content import ens
from genweb.ens.interfaces import IGenwebEnsLayer
from genweb.ens.content.contenidor_ens import IContenidorEns

from genweb.ens.data_access.ens import EnsDataReporter
from genweb.ens.browser import helper


class Search(grok.View):
    grok.name('contenidor_ens_search')
    grok.context(IContenidorEns)
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
    grok.context(IContenidorEns)
    grok.name('contenidor_ens_search_results')
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
