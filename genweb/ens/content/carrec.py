# -*- coding: utf-8 -*-

from collective import dexteritytextindexer
from plone.autoform import directives
from plone.directives import form
from zope import schema
from zope.component.hooks import getSite
from zope.interface import Invalid
from zope.interface import directlyProvides
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

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

    dexteritytextindexer.searchable('carrec_envirtud')
    carrec_envirtud = schema.TextLine(
        title=_(u"En virtud del seu càrrec de:"),
        required=False)

    dexteritytextindexer.searchable('carrec')
    carrec = schema.TextLine(
        title=_(u"Càrrec a l'entitat"),
        required=True)

    data_inici = schema.Date(
        title=_(u"Data d'inici"),
        required=False)

    vigencia = schema.TextLine(
        title=_(u"Vigència"),
        required=False)

    data_fi = schema.Date(
        title=_(u"Data de fi"),
        required=False)

    is_historic = schema.Bool(
        title=_(u"Històric"),
        defaultFactory=lambda: False,
        required=False)

    nomenaments_anteriors = schema.Text(
        title=_(u"Nomenaments anteriors"),
        required=False)

    observacions = schema.Text(
        title=_(u"Observacions"),
        required=False)


def prettify_representant(representant):
    return representant.Title.decode('utf-8') + ' - ' + representant.carrec


def get_vocabulary_representants_upc(context):
    catalog = getSite().portal_catalog
    reporter = CarrecDataReporter(catalog)

    vocabulary_terms = []

    # Get representants from Persones
    vocabulary_terms.append(SimpleTerm(
        title="Persones:",
        value="persones",
        token="persones"))
    vocabulary_terms += [
        SimpleTerm(title=" - " + prettify_representant(
                   representant).encode('utf-8'),
                   value=prettify_representant(representant),
                   token=representant.id)
        for representant in reporter.list_representants('persones')]

    return SimpleVocabulary(vocabulary_terms)


directlyProvides(get_vocabulary_representants_upc, IContextSourceBinder)


def title_constraint(value):
    if value == ("consell-de-direccio", "altres", "persones"):
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

    directives.order_before(title='*')
    dexteritytextindexer.searchable('title')
    title = schema.Choice(
        title=_(u"Cognoms i nom"),
        source=get_vocabulary_representants_upc,
        required=True,
        constraint=title_constraint)
