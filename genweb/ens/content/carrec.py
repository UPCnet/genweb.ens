# -*- coding: utf-8 -*-

from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component.hooks import getSite
from zope.interface import directlyProvides
from zope.schema.interfaces import IContextSourceBinder
from plone.directives import form
from plone.namedfile.field import NamedBlobFile
from collective import dexteritytextindexer

from genweb.ens import _


class ICarrec(form.Schema):
    """
    Càrrec associat a un òrgan d'un ens.
    """

    dexteritytextindexer.searchable('ens')
    ens = schema.TextLine(
        title=_(u"Ens"),
        required=True)

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Cognoms i nom"),
        required=True
    )

    dexteritytextindexer.searchable('carrec')
    carrec = schema.TextLine(
        title=_(u"Càrrec"),
        required=True)

    data_inici = schema.Date(
        title=_(u"Data d'inici"),
        required=False)

    document_nomenament = NamedBlobFile(
        title=_(u"Document de nomenament"),
        description=_(u"Puja un fitxer"),
        required=False)

    data_fi = schema.Date(
        title=_(u"Data de fi"),
        required=False)

    is_historic = schema.Bool(
        title=_(u"Històric"),
        defaultFactory=lambda: False,
        required=False)

    dexteritytextindexer.searchable('observacions')
    observacions = schema.Text(
        title=_(u"Observacions"),
        required=False)


def prettify_representant(representant):
    return representant.Title.decode('utf-8') + ' - ' + representant.carrec


def get_vocabulary_representants_upc(context):
    catalog = getSite().portal_catalog
    return SimpleVocabulary([
        SimpleTerm(title=prettify_representant(representant),
                   value=prettify_representant(representant),
                   token=representant.id)
        for representant in catalog.searchResults(
            portal_type='genweb.ens.representant',
            sort_on='sortable_title',
        )])
directlyProvides(get_vocabulary_representants_upc, IContextSourceBinder)


class ICarrecUPC(ICarrec):
    """
    Càrrec associat a un òrgan d'UPC.
    """

    dexteritytextindexer.searchable('ens')
    ens = schema.TextLine(
        title=_(u"Ens"),
        defaultFactory=lambda: u"UPC",
        readonly=True,
        required=True)

    form.order_before(title='carrec')
    dexteritytextindexer.searchable('title')
    title = schema.Choice(
        title=_(u"Cognoms i nom"),
        source=get_vocabulary_representants_upc,
        required=True
    )
