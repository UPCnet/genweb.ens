from five import grok
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName
from zope.interface import Interface

from genweb.ens.content import ens
from genweb.ens.interfaces import IGenwebEnsLayer

grok.templatedir("ens_views")


class Search(grok.View):
    grok.context(IFolderish)
    grok.name('ens_search')
    grok.layer(IGenwebEnsLayer)

    def get_figura_juridica_vocabulary(self):
        figura_juridica_vocabulary = dict(ens.figura_juridica_value_title)
        figura_juridica_vocabulary.update({'': 'Qualsevol'})
        return figura_juridica_vocabulary.iteritems()

    def get_estat_vocabulary(self):
        estat_vocabulary = dict(ens.estat_value_title)
        estat_vocabulary.update({'': 'Qualsevol'})
        return estat_vocabulary.iteritems()


class SearchResults(grok.View):
    grok.context(Interface)
    grok.name('ens_searchresults')
    grok.layer(IGenwebEnsLayer)

    def parse_search_filters(self):
        search_filters = {}
        try:
            figura_juridica = int(self.request.form.get('figura_juridica', ''))
            search_filters['figura_juridica'] = figura_juridica
        except ValueError:
            pass

        try:
            estat = int(self.request.form.get('estat', ''))
            search_filters['estat'] = estat
        except ValueError:
            pass

        text = self.request.form.get('text', None)
        if text:
            search_filters['SearchableText'] = text

        return search_filters

    def search(self):
        query = {'portal_type': 'genweb.ens.ens', 'sort_on': 'sortable_title'}
        query.update(self.parse_search_filters())

        catalog = getToolByName(self.context, 'portal_catalog')
        return [(ens.getURL(), ens.Title, ens.acronim)
                for ens in catalog.searchResults(query)]
