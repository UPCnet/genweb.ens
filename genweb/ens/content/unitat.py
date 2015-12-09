# -*- coding: utf-8 -*-
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.directives import form

from genweb.ens import _


tipus_gestio_value_title = {
    0: u"Contractació de PDI",
    1: u"Recuperació de l'IVA de factures impagades",
    2: u"Rendició de comptes. SEC 95",
    3: u"Responsabilitats jurídiques",
    4: u"Nomenament de representants",
    5: u"Adscripció o vinculació de personal docent i investigador"}


class IUnitat(form.Schema):
    """
    Unitat de la UPC.
    """

    def get_vocabulary(value_title_dict):
        return SimpleVocabulary([
            SimpleTerm(title=_(title), value=value)
            for value, title in value_title_dict.iteritems()])

    title = schema.TextLine(
        title=_(u"Nom"),
        required=True
    )

    persona = schema.TextLine(
        title=_(u"Persona de referència"),
        required=False)

    tipus_gestio = schema.Choice(
        title=_(u"Tipus"),
        vocabulary=get_vocabulary(tipus_gestio_value_title),
        required=False)
