# -*- coding: utf-8 -*-
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.directives import form

from genweb.ens import _


TIPUS_GOVERN = 1
TIPUS_ASSESSOR = 2
tipus_value_title = {TIPUS_GOVERN:   u"Govern",
                     TIPUS_ASSESSOR: u"Assessor"}


class IOrgan(form.Schema):
    """
    Òrgan de govern associat a un ens.
    """

    def get_vocabulary(value_title_dict):
        return SimpleVocabulary([
            SimpleTerm(title=_(title), value=value)
            for value, title in value_title_dict.iteritems()])

    title = schema.TextLine(
        title=_(u"Nom"),
        required=True
    )

    description = schema.Text(
        title=_(u"Descripció"),
        required=False)

    tipus = schema.Choice(
        title=_(u"Tipus"),
        vocabulary=get_vocabulary(tipus_value_title),
        required=True)
