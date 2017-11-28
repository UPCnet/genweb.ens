# -*- coding: utf-8 -*-

import json

from five import grok
from Products.CMFCore.utils import getToolByName
from zope.interface import Interface

from genweb.ens.interfaces import IGenwebEnsLayer
from genweb.ens.data_access.carrec import CarrecDataReporter
from genweb.ens.browser import helper


class Search(grok.View):
    grok.name('carrec_search')
    grok.context(Interface)
    grok.layer(IGenwebEnsLayer)

    @property
    def carpetes_vocabulary(self):
        return helper.get_carpetes_vocabulary(self)


class SearchResults(grok.View):
    grok.context(Interface)
    grok.name('carrec_search_results')
    grok.layer(IGenwebEnsLayer)

    def parse_search_filters(self):
        search_filters = {}

        text = self.request.form.get('text', None)
        if text:
            search_filters['Title'] = "*{0}*".format(text)

        try:
            carpetes = json.loads(self.request.form.get('carpetes', ''))
            if carpetes:
                search_filters["path"] = {"depth": 3}
                search_filters["path"]["query"] = carpetes
        except ValueError:
            pass

        historics = self.request.form.get('historics', False)
        if not historics or historics == 'false':
            search_filters['is_historic'] = False

        return search_filters

    def search(self):
        reporter = CarrecDataReporter(
            getToolByName(self.context, 'portal_catalog'))
        return reporter.search(self.parse_search_filters())
