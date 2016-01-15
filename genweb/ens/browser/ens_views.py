# -*- coding: utf-8 -*-

import json

from five import grok
from Products.CMFCore.utils import getToolByName
from plone.directives import dexterity
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.interface import Interface
from zope.component import getMultiAdapter

from genweb.theme.browser.views import HomePageBase
from genweb.theme.browser.interfaces import IHomePageView
from genweb.ens import _
from genweb.ens.content import ens
from genweb.ens.interfaces import IGenwebEnsLayer
from genweb.ens.content.ens import IEns
from genweb.ens.content.ens import (get_percentatge_participacio,
                                    get_aportacio, get_quota,
                                    get_capital_social, get_seu_social)
from genweb.ens.data_access.ens import EnsDataReporter


class View(dexterity.DisplayForm):
    grok.context(IEns)
    grok.layer(IGenwebEnsLayer)

    @property
    def percentatge_participacio(self):
        return get_percentatge_participacio(self.context)

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
    def unitats(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_unitat_by_ens_obj(self.context)

    @property
    def acords(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_acord_by_ens_obj(self.context)

    @property
    def estatuts_vigents(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_estatut_by_ens_obj(self.context, is_vigent=True)

    @property
    def estatuts_historics(self):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_estatut_by_ens_obj(self.context, is_vigent=False)

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

    def list_carrecs_by_organ(self, organ, is_historic=None):
        reporter = EnsDataReporter(getToolByName(self, 'portal_catalog'))
        return reporter.list_carrecs_by_organ_grouped_by_ens_obj(
            organ, is_historic=is_historic)


class Search(HomePageBase):
    grok.name('homepage')
    grok.implements(IHomePageView)
    grok.context(INavigationRoot)
    grok.layer(IGenwebEnsLayer)

    def get_figura_juridica_vocabulary(self):
        return [('', _(u"Qualsevol"))] + [
            (value, value) for value in ens.figura_juridica_values]

    def get_estat_vocabulary(self):
        return [('', _(u"Qualsevol"))] + [
            (value, value) for value in ens.estat_values]

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
        """
        Get 3-level folders (e.g. gabinet-juridic in ens/ca/gabinet-juridic/)
        that match a user group name.
        Returns a list of tuples with the following structure:
          - index 0: path of the folder, e.g. /ens/ca/gabinet-juridic
          - index 1: title of the folder, e.g. Gabinet Jurídic
          - index 2: boolean representing whether the folder path matches
            any of the authenticated user's group ids
        """
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
        reporter = EnsDataReporter(
            getToolByName(self.context, 'portal_catalog'))
        return reporter.search(self.parse_search_filters())
