# -*- coding: utf-8 -*-

from five import grok
from zope import schema
from zope.app.container.interfaces import IObjectAddedEvent
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.form.browser.radio import RadioFieldWidget
from plone.directives import form
from plone.dexterity.content import Item
from plone.dexterity.utils import createContentInContainer
from collective import dexteritytextindexer
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

from genweb.ens import _


figura_juridica_values = [
    u"Fundació",
    u"Societat",
    u"Consorci",
    u"Associació",
    u"Sense NIF",
    u"Altra"]

estat_values = [
    _(u"Actiu"),
    u"Pre-Baixa",
    u"Pre-Alta",
    u"Baixa",
    u"Pre-Alta cancel·lada",
    u"Altre"]

institution_type_values = [
    u"Autonòmica",
    u"Estatal",
    u"Local",
    u"Internacional",
    u"Altres"]


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
        fields=['title', 'acronim', 'description', 'objecte_social',
                'estat', 'nif', 'institution_type', 'figura_juridica', 'numero_identificacio',
                'domicili_social_poblacio', 'domicili_social_adreca',
                'adreca_2',
                'telefon', 'fax', 'web',
                'tipologia_upc', 'codi', 'etiquetes',
                'show_dades_identificatives_observacions',
                'dades_identificatives_observacions']
    )

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Denominació completa"),
        required=True
    )

    dexteritytextindexer.searchable('acronim')
    acronim = schema.TextLine(
        title=_(u"Acrònim"),
        required=True,
    )

    dexteritytextindexer.searchable('description')
    description = schema.Text(
        title=_(u"Descripció"),
        required=False)

    dexteritytextindexer.searchable('objecte_social')
    objecte_social = schema.Text(
        title=_(u"Objecte social"),
        required=False)

    dexteritytextindexer.searchable('estat')
    estat = schema.Choice(
        title=_(u"Estat"),
        vocabulary=get_vocabulary(estat_values),
        required=True)

    dexteritytextindexer.searchable('nif')
    nif = schema.TextLine(
        title=_(u"NIF"),
        required=False,
    )

    institution_type = schema.Choice(
        title=_(u"Tipus d'institució"),
        vocabulary=get_vocabulary(institution_type_values),
        required=True,
        default=None)

    figura_juridica = schema.Choice(
        title=_(u"Figura jurídica"),
        vocabulary=get_vocabulary(figura_juridica_values),
        required=True)

    dexteritytextindexer.searchable('numero_identificacio')
    numero_identificacio = schema.TextLine(
        title=_(u"Número d'identificació"),
        required=False)

    dexteritytextindexer.searchable('domicili_social_poblacio')
    domicili_social_poblacio = schema.TextLine(
        title=_(u"Domicili social (població)"),
        required=False)

    dexteritytextindexer.searchable('domicili_social_adreca')
    domicili_social_adreca = schema.TextLine(
        title=_(u"Domicili social (adreça)"),
        required=False)

    dexteritytextindexer.searchable('adreca_2')
    adreca_2 = schema.TextLine(
        title=_(u"Adreça 2"),
        required=False)

    dexteritytextindexer.searchable('telefon')
    telefon = schema.TextLine(
        title=_(u"Telèfon"),
        required=False)

    dexteritytextindexer.searchable('fax')
    fax = schema.TextLine(
        title=_(u"Fax"),
        required=False)

    dexteritytextindexer.searchable('web')
    web = schema.TextLine(
        title=_(u"Web"),
        required=False)

    tipologia_upc = schema.Choice(
        title=_(u"Tipologia UPC"),
        vocabulary=get_vocabulary([
            u"-",
            u"Grup UPC",
            u"Participació Superior",
            u"Entitat Vinculada de Recerca",
            u"Centre Docent",
            u"Institut de Recerca",
            u"Spin-off",
            u"Internacional",
            u"Patronats i Consells Assessors",
            u"Institut de Ciències de l’Educació",
            u"Centres de Recerca",
            u"Departaments",
            u"Grups de Recerca",
            u"Escola de Doctorat",
            u"Càtedres",
            u"Instituts Universitaris de Recerca vinculats",
            u"Centres Docents Adscrits",
            u"Unitats d’Administració i Serveis",
            u"Altra",
            ]),
        required=True)

    dexteritytextindexer.searchable('codi')
    codi = schema.TextLine(
        title=_(u"Codi UPC"),
        required=False)

    # Campo oculto porque se usaran las etiquetas estandar de plone
    dexteritytextindexer.searchable('etiquetes')
    form.omitted('etiquetes')
    etiquetes = schema.Text(
        title=_(u"Etiquetes"),
        required=False)

    show_dades_identificatives_observacions = schema.Bool(
        title=_(u"Show data observations"),
        required = False,
        default = False)

    dexteritytextindexer.searchable('dades_identificatives_observacions')
    dades_identificatives_observacions = schema.Text(
        title=_(u"Observacions"),
        required=False)

    form.fieldset(
        "participacio",
        label=u"Participació de la UPC",
        fields=['aportacio_sn', 'aportacio_import', 'aportacio_moneda',
                'quota_sn', 'quota_import', 'quota_moneda',
                'unitat_carrec', 'percentatge_participacio',
                'nombre_membres',
                'capital_social_sn', 'capital_social_import',
                'capital_social_moneda',
                'show_participacio_observacions',
                'participacio_observacions']
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

    dexteritytextindexer.searchable('nombre_membres')
    nombre_membres = schema.TextLine(
        title=_(u"Membres UPC als òrgans de govern"),
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

    show_participacio_observacions = schema.Bool(
        title = _(u"Show parcicipation observations"),
        required = False,
        default = False)

    dexteritytextindexer.searchable('participacio_observacions')
    participacio_observacions = schema.Text(
        title=_(u"Observacions"),
        required=False)

    form.fieldset(
        "marc_legal",
        label=u"Marc legal",
        fields=['data_constitucio', 'entitats_constituents',
                'entitats_actuals', 'data_entrada',
                'data_entrada_procediment', 'seu_social',
                'seu_social_estranger', 'adscripcio',
                'show_observacions_marc_legal',
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

    dexteritytextindexer.searchable('data_entrada_procediment')
    data_entrada_procediment = schema.Text(
        title=_(u"Procediment d'entrada"),
        required=False)

    seu_social = schema.Choice(
        title=_(u"Seu social"),
        vocabulary=get_vocabulary([
            u"Catalunya",
            u"Resta d'Espanya",
            u"Estranger"]),
        required=False)

    seu_social_estranger = schema.TextLine(
        title=_(u"Seu social a l'estranger"),
        required=False)

    dexteritytextindexer.searchable('adscripcio')
    adscripcio = schema.TextLine(
        title=_(u"Adm. Pública d'adscripció"),
        required=False)

    show_observacions_marc_legal = schema.Bool(
        title = _(u"Show legal framework observations"),
        required = False,
        default = False)

    dexteritytextindexer.searchable('marc_legal_observacions')
    marc_legal_observacions = schema.Text(
        title=_(u"Observacions"),
        required=False)


class Ens(Item):
    implements(IEns)


def create_folder(container, id, title, addable_types):
    folder = createContentInContainer(
        container,
        "Folder",
        id=id,
        title=title,
        exclude_from_nav=True)
    folder_constraints = ISelectableConstrainTypes(folder)
    folder_constraints.setConstrainTypesMode(1)
    folder_constraints.setLocallyAllowedTypes(addable_types)
    folder_constraints.setImmediatelyAddableTypes(addable_types)


@grok.subscribe(IEns, IObjectAddedEvent)
def initialize_ens(ens, event):
    create_folder(
        ens,
        "altres-documents",
        "Altres documents",
        ('Document', 'File', 'Folder', 'Image', 'genweb.ens.document_interes'))

    create_folder(
        ens,
        "reunions",
        "Reunions",
        ('Document', 'File', 'Folder', 'Image', 'genweb.ens.acta_reunio'))


def get_denominacio(ens):
        if ens.acronim:
            return "{0} ({1})".format(
                ens.title.encode("utf-8"),
                ens.acronim.encode("utf-8")).decode("utf-8")
        else:
            return ens.title


def get_percentatge_participacio(ens):
        if ens.percentatge_participacio:
            return "{0:,.2f}%".format(ens.percentatge_participacio)
        else:
            return "-"


def get_aportacio(ens):
    if ens.aportacio_sn is None:
        return "-"
    elif not ens.aportacio_sn:
        return _(u"No")
    else:
        if ens.aportacio_import:
            moneda = "" if ens.aportacio_moneda is None \
                     else " " + ens.aportacio_moneda.encode("utf-8")
            return "{0:,.2f}{1}".format(
                ens.aportacio_import, moneda).decode('utf-8')
        else:
            return _(u"Sí")


def get_quota(ens):
    if ens.quota_sn is None:
        return "-"
    elif not ens.quota_sn:
        return _(u"No")
    else:
        if ens.quota_import:
            moneda = "" if ens.quota_moneda is None \
                else " " + ens.quota_moneda.encode("utf-8")
            return "{0:,.2f}{1}".format(
                ens.quota_import, moneda).decode('utf-8')
        else:
            return _(u"Sí")


def get_capital_social(ens):
    if ens.capital_social_sn is None:
        return "-"
    elif not ens.capital_social_sn:
        return _(u"No")
    else:
        if ens.capital_social_import:
            moneda = "" if ens.capital_social_moneda is None \
                else " " + ens.capital_social_moneda.encode("utf-8")
            return "{0:,.2f}{1}".format(
                ens.capital_social_import, moneda).decode('utf-8')
        else:
            return _(u"Sí")


def get_seu_social(ens):
    if ens.seu_social:
        if ens.seu_social == u"Estranger":
            if ens.seu_social_estranger:
                return ens.seu_social_estranger
            else:
                return ens.seu_social
        else:
            return ens.seu_social
    else:
        return "-"
