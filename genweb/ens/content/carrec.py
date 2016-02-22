# -*- coding: utf-8 -*-

from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component.hooks import getSite
from zope.interface import directlyProvides, Invalid
from zope.schema.interfaces import IContextSourceBinder
from plone.directives import form
from collective import dexteritytextindexer

from genweb.ens import _
from genweb.ens.data_access.carrec import CarrecDataReporter


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
        required=True)

    dexteritytextindexer.searchable('carrec')
    carrec = schema.TextLine(
        title=_(u"Càrrec"),
        required=True)

    data_inici = schema.Date(
        title=_(u"Data d'inici"),
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
    reporter = CarrecDataReporter(catalog)

    vocabulary_terms = []
    # Get representants from Consell de Direcció
    vocabulary_terms.append(SimpleTerm(
        title="Consell de direcció:",
        value="consell-de-direccio",
        token="consell-de-direccio"))
    vocabulary_terms += [
        SimpleTerm(title=" - " + prettify_representant(
                   representant).encode('utf-8'),
                   value=prettify_representant(representant),
                   token=representant.getRID())
        for representant in reporter.list_representants('consell-de-direccio')]

    # Get representants from Altres
    vocabulary_terms.append(SimpleTerm(
        title="Altres:",
        value="altres",
        token="altres"))
    vocabulary_terms += [
        SimpleTerm(title=" - " + prettify_representant(
                   representant).encode('utf-8'),
                   value=prettify_representant(representant),
                   token=representant.id)
        for representant in reporter.list_representants('altres')]

    return SimpleVocabulary(vocabulary_terms)
directlyProvides(get_vocabulary_representants_upc, IContextSourceBinder)


def title_constraint(value):
    if value in ("consell-de-direccio", "altres"):
        raise Invalid(_(u"Cal que introduïu cognoms i nom"))
    return True


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
        required=True,
        constraint=title_constraint)
