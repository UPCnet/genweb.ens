import json

from five import grok
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName
from zope.interface import Interface
from zope.component import getMultiAdapter

from genweb.ens.content import ens
from genweb.ens.interfaces import IGenwebEnsLayer

grok.templatedir("ens_views")


class Search(grok.View):
    grok.context(IFolderish)
    grok.name('search-ens')
    grok.layer(IGenwebEnsLayer)

    def get_figura_juridica_vocabulary(self):
        figura_juridica_vocabulary = dict(ens.figura_juridica_value_title)
        figura_juridica_vocabulary.update({'': 'Qualsevol'})
        return figura_juridica_vocabulary.iteritems()

    def get_estat_vocabulary(self):
        estat_vocabulary = dict(ens.estat_value_title)
        estat_vocabulary.update({'': 'Qualsevol'})
        return estat_vocabulary.iteritems()

    def is_user_folder(self, folder):
        portal_state = getMultiAdapter(
            (self.context, self.request), name="plone_portal_state")
        if portal_state.anonymous():
            return False
        elif not portal_state.member().getUser().getGroups():
            return False
        else:
            group_ids = portal_state.member().getUser().getGroupIds()
            return any(folder.getPath().endswith(user_folder_name)
                       for user_folder_name in group_ids)

    def get_user_folders(self):
        portal_state = getMultiAdapter(
            (self.context, self.request), name="plone_portal_state")
        if portal_state.anonymous():
            return set()
        elif not portal_state.member().getUser().getGroups():
            return set()
        else:
            return set(portal_state.member().getUser().getGroupIds())

    def get_carpetes_vocabulary(self):
        user_folders = self.get_user_folders()
        catalog = getToolByName(self, 'portal_catalog')
        return [(folder.getPath(),
                 folder.Title,
                 folder.getPath().split('/')[-1] in user_folders)

                for folder in catalog.searchResults(
                    portal_type='Folder',
                    sort_on='sortable_title',
                    path={
                        'query': '/',
                        'depth': 3
                    })]


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

        try:
            carpetes = json.loads(self.request.form.get('carpetes', None))
            if carpetes:
                search_filters["path"] = {"depth": 1}
                search_filters["path"]["query"] = [
                    carpeta for carpeta in carpetes]
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
