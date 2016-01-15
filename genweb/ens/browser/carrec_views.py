# -*- coding: utf-8 -*-

from five import grok
from Products.CMFCore.utils import getToolByName
from zope.interface import Interface

from genweb.ens.interfaces import IGenwebEnsLayer
from genweb.ens.data_access.carrec import CarrecDataReporter


class Search(grok.View):

    grok.name('carrec_search')
    grok.context(Interface)
    grok.layer(IGenwebEnsLayer)


class SearchResults(grok.View):
    grok.context(Interface)
    grok.name('carrec_search_results')
    grok.layer(IGenwebEnsLayer)

    def parse_search_filters(self):
        search_filters = {}

        text = self.request.form.get('text', None)
        if text:
            search_filters['Title'] = "*{0}*".format(text)

        historics = self.request.form.get('historics', False)
        if not historics or historics == 'false':
            search_filters['is_historic'] = False

        return search_filters

    def search(self):
        reporter = CarrecDataReporter(
            getToolByName(self.context, 'portal_catalog'))
        return reporter.search(self.parse_search_filters())
