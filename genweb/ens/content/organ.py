# -*- coding: utf-8 -*-

from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.directives import form
from collective import dexteritytextindexer

from genweb.ens import _


class IOrgan(form.Schema):
    """
    Òrgan de govern associat a un ens.
    """

    def get_vocabulary(values):
        return SimpleVocabulary([
            SimpleTerm(title=_(value), value=value, token=token)
            for token, value in enumerate(values)])

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Nom"),
        required=True
    )

    dexteritytextindexer.searchable('description')
    description = schema.Text(
        title=_(u"Descripció"),
        required=False)

    dexteritytextindexer.searchable('composicio')
    composicio = schema.Text(
        title=_(u"Composició"),
        required=False)

    tipus = schema.Choice(
        title=_(u"Tipus"),
        vocabulary=get_vocabulary([
            u"Govern",
            u"Assessor"]),
        required=True)

    is_historic = schema.Bool(
        title=_(u"Històric"),
        defaultFactory=lambda: False,
        required=False)
