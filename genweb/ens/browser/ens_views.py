from plone.directives import dexterity
from five import grok
from Products.CMFCore.utils import getToolByName

from genweb.ens.interfaces import IGenwebEnsLayer
from genweb.ens.content.ens import IEns
from genweb.ens.content.ens import (get_percentatge_participacio,
                                    get_aportacio, get_quota,
                                    get_capital_social, get_seu_social)
from genweb.ens.data_access.ens import EnsDataReporter


class View(dexterity.DisplayForm):
    grok.context(IEns)
    grok.template('view')
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
