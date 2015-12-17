# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.form.browser.radio import RadioFieldWidget
from plone.directives import form, dexterity
from plone.dexterity.content import Item
from five import grok
from collective import dexteritytextindexer
from Products.CMFCore.utils import getToolByName

from genweb.ens import _


figura_juridica_values = [
    u"Fundació",
    u"Societat",
    u"Consorci",
    u"Sense NIF",
    u"Altra"]

estat_values = [
    u"Actiu",
    u"Pre-Baixa",
    u"Pre-Alta",
    u"Baixa",
    u"Pre-alta cancel·lada",
    u"Altre"]


class IEns(form.Schema):
    """
    Organització com ara una universitat o una empresa.
    """

    def get_vocabulary(values):
        return SimpleVocabulary([
            SimpleTerm(title=_(value), value=value, token=token)
            for token, value in enumerate(values)])

    form.fieldset(
        "dades_identificatives",
        label=u"Dades identificatives",
        fields=['title', 'description', 'acronim', 'codi', 'nif',
                'figura_juridica', 'numero_identificacio', 'estat',
                'domicili_social', 'adreca_oficines', 'web', 'tipologia']
    )

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Denominació complerta"),
        required=True
    )

    dexteritytextindexer.searchable('description')
    description = schema.Text(
        title=_(u"Descripció"),
        required=False)

    dexteritytextindexer.searchable('acronim')
    acronim = schema.TextLine(
        title=_(u"Acrònim"),
        required=True,
    )

    dexteritytextindexer.searchable('codi')
    codi = schema.TextLine(
        title=_(u"Codi de classificació"),
        required=False)

    dexteritytextindexer.searchable('nif')
    nif = schema.TextLine(
        title=_(u"NIF"),
        required=False,
    )

    figura_juridica = schema.Choice(
        title=_(u"Figura jurídica"),
        vocabulary=get_vocabulary(figura_juridica_values),
        required=True)

    dexteritytextindexer.searchable('numero_identificacio')
    numero_identificacio = schema.TextLine(
        title=_(u"Número d'identificació"),
        required=False)

    estat = schema.Choice(
        title=_(u"Estat"),
        vocabulary=get_vocabulary(estat_values),
        required=True)

    dexteritytextindexer.searchable('domicili_social')
    domicili_social = schema.TextLine(
        title=_(u"Domicili social"),
        required=False)

    dexteritytextindexer.searchable('adreca_oficines')
    adreca_oficines = schema.TextLine(
        title=_(u"Adreça oficines"),
        required=False)

    dexteritytextindexer.searchable('web')
    web = schema.TextLine(
        title=_(u"Web"),
        description=_(u"Direcció de la pàgina web"),
        required=False)

    tipologia = schema.Choice(
        title=_(u"Tipologia"),
        vocabulary=get_vocabulary([
            u"Grup UPC",
            u"Participació Superior",
            u"Entitat Vinculada de Recerca",
            u"Centre Docent",
            u"Institut de Recerca",
            u"Spin-off",
            u"Internacional",
            u"Altra"]),
        required=True)

    form.fieldset(
        "participacio",
        label=u"Participació",
        fields=['aportacio_sn', 'aportacio_import', 'quota_sn', 'quota_import',
                'unitat_carrec', 'participacio_capital',
                'participacio_observacions']
    )

    form.widget(aportacio_sn=RadioFieldWidget)
    aportacio_sn = schema.Choice(
        title=_(u"Aportació inicial"),
        vocabulary=SimpleVocabulary(
            [SimpleTerm(title=_(u"Sí"), value=True),
             SimpleTerm(title=_(u"No"), value=False)]),
        required=False,
    )

    aportacio_import = schema.Float(
        title=_(u"Import"),
        required=False)

    form.widget(quota_sn=RadioFieldWidget)
    quota_sn = schema.Choice(
        title=_(u"Quota"),
        vocabulary=SimpleVocabulary(
            [SimpleTerm(title=_(u"Sí"), value=True),
             SimpleTerm(title=_(u"No"), value=False)]),
        required=False,
    )

    quota_import = schema.Float(
        title=_(u"Import"),
        required=False)

    dexteritytextindexer.searchable('unitat_carrec')
    unitat_carrec = schema.TextLine(
        title=_(u"Unitat de càrrec"),
        required=False)

    participacio_capital = schema.Float(
        title=_(u"Capital social o fons patrimonial"),
        required=False)

    dexteritytextindexer.searchable('participacio_observacions')
    participacio_observacions = schema.Text(
        title=_(u"Observacions"),
        required=False)

    form.fieldset(
        "marc_legal",
        label=u"Marc legal",
        fields=['data_constitucio', 'entitats_constituents',
                'entitats_actuals', 'data_entrada', 'seu_social',
                'marc_legal_observacions']
    )

    data_constitucio = schema.Date(
        title=_(u"Data de constitució"),
        required=False)

    dexteritytextindexer.searchable('entitats_constituents')
    entitats_constituents = schema.Text(
        title=_(u"Entitats constituents"),
        required=False)

    dexteritytextindexer.searchable('entitats_actuals')
    entitats_actuals = schema.Text(
        title=_(u"Entitats actuals"),
        required=False)

    data_entrada = schema.Date(
        title=_(u"Data d'entrada UPC"),
        required=False)

    seu_social = schema.Choice(
        title=_(u"Seu social"),
        vocabulary=get_vocabulary([
            u"CAT: Catalunya",
            u"ESP: Altres localitats d'Espanya",
            u"EST: Estranger"]),
        required=False)

    dexteritytextindexer.searchable('marc_legal_observacions')
    marc_legal_observacions = schema.Text(
        title=_(u"Observacions"),
        required=False)


class Ens(Item):
    implements(IEns)


class View(dexterity.DisplayForm):
    grok.context(IEns)
    grok.template('view')

    def get_aportacio(self):
        if self.context.aportacio_sn is None:
            return "-"
        elif not self.context.aportacio_sn:
            return _(u"No")
        else:
            if self.context.aportacio_import:
                return "{0:,.2f} EUR".format(self.context.aportacio_import)
            else:
                return _(u"Sí (desconeguda)")

    def get_quota(self):
        if self.context.quota_sn is None:
            return "-"
        elif not self.context.quota_sn:
            return _(u"No")
        else:
            if self.context.quota_import:
                return "{0:,.2f} EUR".format(self.context.quota_import)
            else:
                return _(u"Sí (desconeguda)")

    def get_capital_social(self):
        if self.context.participacio_capital is None:
            return "-"
        else:
            return "{0:,.2f} EUR".format(self.context.participacio_capital)

    def get_percentatges_participacio_obj(self):
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        return [percentatge.getObject()
                for percentatge in catalog.searchResults(
            portal_type='genweb.ens.percentatge_participacio',
            sort_on='sortable_title',
            path={
                'query': folder_path,
                'depth': 1
            })]

    def get_unitats_obj(self):
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        return [unitat.getObject() for unitat in catalog.searchResults(
            portal_type='genweb.ens.unitat',
            sort_on='sortable_title',
            path={
                'query': folder_path,
                'depth': 1
            })]

    def get_acords_obj(self):
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        return [acord.getObject() for acord in catalog.searchResults(
            portal_type='genweb.ens.acord',
            sort_on='getObjPositionInParent',
            path={
                'query': folder_path,
                'depth': 2
            })]

    def get_estatuts_vigents_obj(self):
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        return [estatut.getObject() for estatut in catalog.searchResults(
            portal_type='genweb.ens.estatut',
            is_vigent=True,
            # TODO Handle the cases where data is None (the current
            #      implementation just ignores those instances)
            sort_on='data',
            sort_order='descending',
            path={
                'query': folder_path,
                'depth': 1
            })]

    def get_estatuts_anteriors_obj(self):
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        return [estatut.getObject() for estatut in catalog.searchResults(
            portal_type='genweb.ens.estatut',
            is_vigent=False,
            # TODO Handle the cases where data is None (the current
            #      implementation just ignores those instances)
            sort_on='data',
            sort_order='descending',
            path={
                'query': folder_path,
                'depth': 1
            })]

    def get_escriptures_obj(self):
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        return [escriptura.getObject() for escriptura in catalog.searchResults(
            portal_type='genweb.ens.escriptura_publica',
            sort_on='getObjPositionInParent',
            path={
                'query': folder_path,
                'depth': 1
            })]

    def get_documents_interes_obj(self):
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        return [document.getObject() for document in catalog.searchResults(
            portal_type='genweb.ens.document_interes',
            sort_on='getObjPositionInParent',
            path={
                'query': folder_path,
                'depth': 1
            })]

    def get_convenis_obj(self):
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        return [conveni.getObject() for conveni in catalog.searchResults(
            portal_type='genweb.ens.conveni',
            sort_on='getObjPositionInParent',
            path={
                'query': folder_path,
                'depth': 1
            })]

    def get_organs_govern(self):
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        return [organ for organ in catalog.searchResults(
            portal_type='genweb.ens.organ',
            tipus="Govern",
            sort_on='getObjPositionInParent',
            path={
                'query': folder_path,
                'depth': 1
            })]

    def get_organs_assessors(self):
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        return [organ for organ in catalog.searchResults(
            portal_type='genweb.ens.organ',
            tipus="Assessor",
            sort_on='getObjPositionInParent',
            path={
                'query': folder_path,
                'depth': 1
            })]

    def get_directius_obj(self):
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        return [carrec.getObject() for carrec in catalog.searchResults(
            portal_type='genweb.ens.persona_directiu',
            sort_on='sortable_title',
            path={
                'query': folder_path,
                'depth': 2
            })]

    def get_contactes_obj(self):
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        return [carrec.getObject() for carrec in catalog.searchResults(
            portal_type='genweb.ens.persona_contacte',
            sort_on='sortable_title',
            path={
                'query': folder_path,
                'depth': 2
            })]

    def get_carrecs_by_organ_grouped_by_ens(self, organ, is_historic=None):
        carrecs_by_organ = []

        catalog = getToolByName(self, 'portal_catalog')
        query = {
            'portal_type': 'genweb.ens.carrec_upc',
            'sort_on': 'sortable_title',
            'path': {
                'query': organ.getPath(),
                'depth': 1
            }}
        if is_historic is not None:
            query['is_historic'] = is_historic

        # Retrieve UPC carrecs
        carrecs_upc = [carrec for carrec in catalog.searchResults(query)]
        if carrecs_upc:
            carrecs_by_organ.append(("UPC", carrecs_upc))

        # Retrieve not-UPC carrecs
        query['portal_type'] = 'genweb.ens.carrec'
        carrecs_by_ens = {}
        for carrec in catalog.searchResults(query):
            if carrec.ens not in carrecs_by_ens:
                carrecs_by_ens[carrec.ens] = []
            carrecs_by_ens[carrec.ens].append(carrec)

        # Append not-UPC carrecs
        for ens, carrecs in carrecs_by_ens.iteritems():
            carrecs_by_organ.append((ens, carrecs))

        return carrecs_by_organ
