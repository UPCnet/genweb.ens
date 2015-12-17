# -*- coding: utf-8 -*-

import json

from five import grok
from Products.CMFCore.utils import getToolByName
from zope.interface import Interface
from zope.component import getMultiAdapter

from genweb.ens.content import ens
from genweb.ens.interfaces import IGenwebEnsLayer

from genweb.theme.browser.views import HomePageBase
from genweb.theme.browser.interfaces import IHomePageView
from plone.app.layout.navigation.interfaces import INavigationRoot

from genweb.ens import _


class Search(HomePageBase):
    grok.name('homepage')
    grok.implements(IHomePageView)
    grok.context(INavigationRoot)
    grok.template('search')
    grok.layer(IGenwebEnsLayer)

    def get_figura_juridica_vocabulary(self):
        figura_juridica_vocabulary = dict([(value, value) for value in ens.figura_juridica_values])
        figura_juridica_vocabulary.update({'': _(u"Qualsevol")})
        return figura_juridica_vocabulary.iteritems()

    def get_estat_vocabulary(self):
        estat_vocabulary = dict([(value, value) for value in ens.estat_values])
        estat_vocabulary.update({'': _(u"Qualsevol")})
        return estat_vocabulary.iteritems()

    def is_authenticated(self):
        portal_state = getMultiAdapter(
            (self.context, self.request), name="plone_portal_state")
        return not portal_state.anonymous()

    def get_portal_groups(self):
        acl_users = getToolByName(self, 'acl_users')
        return [group_id for group_id in acl_users.source_groups.getGroupIds()]

    def get_user_groups(self):
        portal_state = getMultiAdapter(
            (self.context, self.request), name="plone_portal_state")
        if portal_state.anonymous():
            return set()
        elif not portal_state.member().getUser().getGroups():
            return set()
        else:
            return set(portal_state.member().getUser().getGroupIds())

    def get_carpetes_vocabulary(self):
        portal_groups = self.get_portal_groups()
        user_groups = self.get_user_groups()
        catalog = getToolByName(self, 'portal_catalog')
        return [(folder.getPath(),
                 folder.Title,
                 folder.getPath().split('/')[-1] in user_groups)

                for folder in catalog.searchResults(
                    portal_type='Folder',
                    sort_on='sortable_title',
                    path={
                        'query': '/',
                        'depth': 3
                    }) if folder.getPath().split('/')[-1] in portal_groups]


class SearchResults(grok.View):
    grok.context(Interface)
    grok.name('ens_searchresults')
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
            carpetes = json.loads(self.request.form.get('carpetes', None))
            if carpetes:
                search_filters["path"] = {"depth": 1}
                search_filters["path"]["query"] = [
                    carpeta for carpeta in carpetes]
        except ValueError:
            pass

        text = self.request.form.get('text', None)
        if text:
            search_filters['SearchableText'] = "*{0}*".format(text)

        return search_filters

    def search(self):
        query = {'portal_type': 'genweb.ens.ens', 'sort_on': 'sortable_title'}
        query.update(self.parse_search_filters())

        catalog = getToolByName(self.context, 'portal_catalog')
        return [(ens.getURL(), ens.Title, ens.acronim)
                for ens in catalog.searchResults(query)]
