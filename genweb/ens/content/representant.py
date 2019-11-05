# -*- coding: utf-8 -*-

from collective import dexteritytextindexer
from zope import schema
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from genweb.ens import _
from genweb.ens.content.persona import IPersona

carrecs = [
    u"PDI",
    u"PAS",
    u"Estudiant",
    u"Extern",
    u"Extern CS"]


class IRepresentant(IPersona):
    """
    Càrrec que pot representar UPC en algun ens
    """

    def get_vocabulary(values):
        return SimpleVocabulary([
            SimpleTerm(title=_(value), value=value, token=token)
            for token, value in enumerate(values)])

    dexteritytextindexer.searchable('carrec')
    carrec = schema.Choice(
        title=_(u"Col·lectiu"),
        vocabulary=get_vocabulary(carrecs),
        required=False
    )
