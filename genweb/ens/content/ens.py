# -*- coding: utf-8 -*-

import datetime

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
                'domicili_social',
                'adreca_oficines_1', 'adreca_oficines_1_observacions',
                'adreca_oficines_2', 'adreca_oficines_2_observacions',
                'telefon', 'web', 'tipologia_upc', 'anotacions']
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

    dexteritytextindexer.searchable('adreca_oficines_1')
    adreca_oficines_1 = schema.TextLine(
        title=_(u"Adreça oficines 1"),
        required=False)

    dexteritytextindexer.searchable('adreca_oficines_1_observacions')
    adreca_oficines_1_observacions = schema.TextLine(
        title=_(u"Observacions"),
        required=False)

    dexteritytextindexer.searchable('adreca_oficines_2')
    adreca_oficines_2 = schema.TextLine(
        title=_(u"Adreça oficines 2"),
        required=False)

    dexteritytextindexer.searchable('adreca_oficines_2_observacions')
    adreca_oficines_2_observacions = schema.TextLine(
        title=_(u"Observacions"),
        required=False)

    dexteritytextindexer.searchable('telefon')
    telefon = schema.TextLine(
        title=_(u"Telèfon"),
        required=False)

    dexteritytextindexer.searchable('web')
    web = schema.TextLine(
        title=_(u"Web"),
        description=_(u"Direcció de la pàgina web"),
        required=False)

    tipologia_upc = schema.Choice(
        title=_(u"Tipologia UPC"),
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

    dexteritytextindexer.searchable('anotacions')
    anotacions = schema.Text(
        title=_(u"Anotacions"),
        required=False)

    form.fieldset(
        "participacio",
        label=u"Participació de la UPC",
        fields=['aportacio_sn', 'aportacio_import', 'aportacio_moneda',
                'quota_sn', 'quota_import', 'quota_moneda',
                'unitat_carrec', 'percentatge_participacio',
                'percentatge_participacio_observacions',
                'capital_social_sn', 'capital_social_import',
                'capital_social_moneda', 'participacio_observacions']
    )

    form.widget(aportacio_sn=RadioFieldWidget)
    aportacio_sn = schema.Choice(
        title=_(u"Aportació inicial"),
        vocabulary=SimpleVocabulary(
            [SimpleTerm(title=_(u"Sí"), value=True),
             SimpleTerm(title=_(u"No"), value=False),
             SimpleTerm(title=_(u"Desconeguda"), value=None)]),
        required=False,
    )

    aportacio_import = schema.Float(
        title=_(u"Import"),
        required=False)

    aportacio_moneda = schema.TextLine(
        title=_(u"Moneda"),
        required=False)

    form.widget(quota_sn=RadioFieldWidget)
    quota_sn = schema.Choice(
        title=_(u"Quota"),
        vocabulary=SimpleVocabulary(
            [SimpleTerm(title=_(u"Sí"), value=True),
             SimpleTerm(title=_(u"No"), value=False),
             SimpleTerm(title=_(u"Desconeguda"), value=None)]),
        required=False,
    )

    quota_import = schema.Float(
        title=_(u"Import"),
        required=False)

    quota_moneda = schema.TextLine(
        title=_(u"Moneda"),
        required=False)

    dexteritytextindexer.searchable('unitat_carrec')
    unitat_carrec = schema.TextLine(
        title=_(u"Unitat de càrrec"),
        required=False)

    percentatge_participacio = schema.Float(
        title=_(u"Percentatge de participació"),
        required=False)

    dexteritytextindexer.searchable('percentatge_participacio_observacions')
    percentatge_participacio_observacions = schema.Text(
        title=_(u"Observacions"),
        required=False)

    form.widget(capital_social_sn=RadioFieldWidget)
    capital_social_sn = schema.Choice(
        title=_(u"Participació en capital social o fons patrimonial"),
        vocabulary=SimpleVocabulary(
            [SimpleTerm(title=_(u"Sí"), value=True),
             SimpleTerm(title=_(u"No"), value=False),
             SimpleTerm(title=_(u"Desconeguda"), value=None)]),
        required=False,
    )

    capital_social_import = schema.Float(
        title=_(u"Import"),
        required=False)

    capital_social_moneda = schema.TextLine(
        title=_(u"Moneda"),
        required=False)

    dexteritytextindexer.searchable('participacio_observacions')
    participacio_observacions = schema.Text(
        title=_(u"Observacions"),
        required=False)

    form.fieldset(
        "marc_legal",
        label=u"Marc legal",
        fields=['data_constitucio', 'entitats_constituents',
                'entitats_actuals', 'data_entrada',
                'data_entrada_descripcio', 'seu_social',
                'seu_social_estranger', 'marc_legal_observacions']
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

    dexteritytextindexer.searchable('data_entrada_descripcio')
    data_entrada_descripcio = schema.Text(
        title=_(u"Descripció"),
        required=False)

    seu_social = schema.Choice(
        title=_(u"Seu social"),
        vocabulary=get_vocabulary([
            u"Catalunya",
            u"Resta d'Espanya",
            u"Estranger"]),
        required=False)

    seu_social_estranger = schema.TextLine(
        title=_(u"Seu social en el estranger"),
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

    @property
    def percentatge_participacio(self):
        if self.context.percentatge_participacio:
            return "{0:,.2f}%".format(self.context.percentatge_participacio)
        else:
            return "-"

    @property
    def aportacio(self):
        if self.context.aportacio_sn is None:
            return "-"
        elif not self.context.aportacio_sn:
            return _(u"No")
        else:
            if self.context.aportacio_import:
                moneda = "" if self.context.aportacio_moneda is None \
                    else " " + self.context.aportacio_moneda.encode("utf-8")
                return "{0:,.2f} {1}".format(
                    self.context.aportacio_import,
                    moneda)
            else:
                return _(u"Sí")

    @property
    def quota(self):
        if self.context.quota_sn is None:
            return "-"
        elif not self.context.quota_sn:
            return _(u"No")
        else:
            if self.context.quota_import:
                moneda = "" if self.context.quota_moneda is None \
                    else " " + self.context.quota_moneda.encode("utf-8")
                return "{0:,.2f} {1}".format(self.context.quota_import, moneda)
            else:
                return _(u"Sí")

    @property
    def capital_social(self):
        if self.context.capital_social_sn is None:
            return "-"
        elif not self.context.capital_social_sn:
            return _(u"No")
        else:
            if self.context.capital_social_import:
                moneda = "" if self.context.capital_social_moneda is None \
                    else " " + self.context.capital_social_moneda.encode(
                        "utf-8")
                return "{0:,.2f} {1}".format(
                    self.context.capital_social_import,
                    moneda)
            else:
                return _(u"Sí")

    @property
    def seu_social(self):
        if self.context.seu_social:
            if self.context.seu_social == u"Estranger":
                if self.context.seu_social_estranger:
                    return self.context.seu_social_estranger
                else:
                    return self.context.seu_social
            else:
                return self.context.seu_social
        else:
            return "-"

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
            sort_on='organ',
            path={
                'query': folder_path,
                'depth': 1
            })]

    def get_estatuts_obj(self, is_vigent=True):
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        # TODO Optimise this code so that the sorting is performed by ZODB
        return sorted([
            estatut.getObject() for estatut in catalog.searchResults(
                portal_type='genweb.ens.estatut',
                is_vigent=is_vigent,
                path={
                    'query': folder_path,
                    'depth': 1
                })],
            key=lambda e: e.data if e.data else datetime.date.min,
            reverse=True)

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

    def get_actes_reunio_obj(self):
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        return [acta.getObject() for acta in catalog.searchResults(
            portal_type='genweb.ens.acta_reunio',
            sort_on='sortable_title',
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

    def get_carrecs_by_organ_grouped_by_ens_obj(self, organ, is_historic=None):
        carrecs_by_organ = []

        catalog = getToolByName(self, 'portal_catalog')
        query = {
            'portal_type': 'genweb.ens.carrec_upc',
            'sort_on': 'carrec',
            'path': {
                'query': organ.getPath(),
                'depth': 1
            }}
        if is_historic is not None:
            query['is_historic'] = is_historic

        # Retrieve UPC carrecs
        carrecs_upc = [carrec.getObject()
                       for carrec in catalog.searchResults(query)]
        if carrecs_upc:
            carrecs_by_organ.append(("UPC", carrecs_upc))

        # Retrieve not-UPC carrecs
        query['portal_type'] = 'genweb.ens.carrec'
        carrecs_by_ens = {}
        for carrec in catalog.searchResults(query):
            carrec_obj = carrec.getObject()
            if carrec_obj.ens not in carrecs_by_ens:
                carrecs_by_ens[carrec_obj.ens] = []
            carrecs_by_ens[carrec_obj.ens].append(carrec_obj)

        # Append not-UPC carrecs grouped by their alphabetically sorted ens
        for ens, carrecs in sorted(
                carrecs_by_ens.iteritems(), key=lambda e: e[0].lower()):
            carrecs_by_organ.append((ens, carrecs))

        return carrecs_by_organ
