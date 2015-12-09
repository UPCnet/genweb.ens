# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.directives import form, dexterity
from plone.dexterity.content import Item
from five import grok
from Products.CMFCore.utils import getToolByName

from genweb.ens import _
from genweb.ens import content


figura_juridica_value_title = {1: u"Fundació",
                               2: u"Societat",
                               3: u"Consorci",
                               4: u"Associació",
                               5: u"Sense NIF",
                               6: u"Altra"}

estat_value_title = {1: u"Actiu",
                     2: u"Pre-Baixa",
                     3: u"Pre-Alta",
                     4: u"Baixa",
                     5: u"Pre-alta cancel·lada",
                     6: u"Altre"}

tipologia_value_title = {1: u"Grup UPC",
                         2: u"Participació Superior",
                         3: u"Entitat Vinculada de Recerca",
                         4: u"Centre Docent",
                         5: u"Institut de Recerca",
                         6: u"Spin-off",
                         7: u"Internacional",
                         8: u"Altra"}

seu_social_value_title = {1: u"CAT: Catalunya",
                          2: u"ESP: Altres localitats d'Espanya",
                          3: u"EST: Estranger"}


class IEns(form.Schema):
    """
    Organització com ara una unversitat o una empresa.
    """

    def get_vocabulary(value_title_dict):
        return SimpleVocabulary([
            SimpleTerm(title=_(title), value=value)
            for value, title in value_title_dict.iteritems()])

    form.fieldset(
        "dades_identificatives",
        label=u"Dades identificatives",
        fields=['title', 'description', 'acronim', 'codi', 'nif',
                'figura_juridica', 'estat', 'domicili_social',
                'adreca_oficines', 'web', 'tipologia']
    )

    title = schema.TextLine(
        title=_(u"Denominació complerta"),
        required=True
    )

    description = schema.Text(
        title=_(u"Descripció"),
        required=False)

    acronim = schema.TextLine(
        title=_(u"Acrònim"),
        required=True,
    )

    codi = schema.TextLine(
        title=_(u"Codi de classificació"),
        required=False)

    nif = schema.TextLine(
        title=_(u"NIF"),
        required=False,
    )

    figura_juridica = schema.Choice(
        title=_(u"Figura jurídica"),
        vocabulary=get_vocabulary(figura_juridica_value_title),
        required=True)

    estat = schema.Choice(
        title=_(u"Estat"),
        vocabulary=get_vocabulary(estat_value_title),
        required=True)

    domicili_social = schema.TextLine(
        title=_(u"Domicili social"),
        required=False)

    adreca_oficines = schema.TextLine(
        title=_(u"Adreça oficines"),
        required=False)

    web = schema.TextLine(
        title=_(u"Web"),
        description=_(u"Direcció de la pàgina web"),
        required=False)

    tipologia = schema.Choice(
        title=_(u"Tipologia"),
        vocabulary=get_vocabulary(tipologia_value_title),
        required=True)

    form.fieldset(
        "participacio",
        label=u"Participació",
        fields=['aportacio', 'quota', 'unitat_carrec', 'participacio_capital',
                'participacio_observacions']
    )

    aportacio = schema.TextLine(
        title=_(u"Aportació inicial"),
        required=False)

    quota = schema.TextLine(
        title=_(u"Quota"),
        required=False)

    unitat_carrec = schema.TextLine(
        title=_(u"Unitat de càrrec"),
        required=False)

    participacio_capital = schema.Float(
        title=_(u"Capital social o fons patrimonial"),
        required=False)

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
        title=_(u"Data de constitucio"),
        required=False)

    entitats_constituents = schema.Text(
        title=_(u"Entitats constituents"),
        required=False)

    entitats_actuals = schema.Text(
        title=_(u"Entitats actuals"),
        required=False)

    data_entrada = schema.Date(
        title=_(u"Data d'entrada UPC"),
        required=False)

    seu_social = schema.Choice(
        title=_(u"Seu social"),
        vocabulary=get_vocabulary(seu_social_value_title),
        required=False)

    marc_legal_observacions = schema.Text(
        title=_(u"Observacions"),
        required=False)


class Ens(Item):
    implements(IEns)


class View(dexterity.DisplayForm):
    grok.context(IEns)
    grok.template('view')

    def get_figura_juridica_title(self, figura_juridica_value):
        return _(figura_juridica_value_title[figura_juridica_value])

    def get_estat_title(self, estat_value):
        return _(estat_value_title[estat_value])

    def get_tipologia_title(self, tipologia_value):
        return _(tipologia_value_title[tipologia_value])

    def get_seu_social_title(self, seu_social_value):
        if seu_social_value in seu_social_value_title:
            return _(seu_social_value_title[seu_social_value])
        return None

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

    def get_unitats(self):
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        return [unitat for unitat in catalog.searchResults(
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
            portal_type='genweb.ens.escriptura',
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
            tipus=content.organ.TIPUS_GOVERN,
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
            tipus=content.organ.TIPUS_ASSESSOR,
            sort_on='getObjPositionInParent',
            path={
                'query': folder_path,
                'depth': 1
            })]

    def get_directius(self):
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        return [carrec for carrec in catalog.searchResults(
            portal_type='genweb.ens.carrec',
            is_directiu=True,
            sort_on='getObjPositionInParent',
            path={
                'query': folder_path,
                'depth': 2
            })]

    def get_contactes(self):
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        return [carrec for carrec in catalog.searchResults(
            portal_type='genweb.ens.carrec',
            is_contacte=True,
            sort_on='getObjPositionInParent',
            path={
                'query': folder_path,
                'depth': 2
            })]

    def get_carrecs_by_organ(self, organ):
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = organ.getPath()

        return [carrec for carrec in catalog.searchResults(
            portal_type='genweb.ens.carrec',
            sort_on='getObjPositionInParent',
            path={
                'query': folder_path,
                'depth': 1
            })]
