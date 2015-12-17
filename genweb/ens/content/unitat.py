# -*- coding: utf-8 -*-
from zope import schema
from collective import dexteritytextindexer
from plone.directives import form

from genweb.ens import _


class IUnitat(form.Schema):
    """
    Unitat de la UPC.
    """

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Nom"),
        required=True
    )

    dexteritytextindexer.searchable('persona')
    persona = schema.TextLine(
        title=_(u"Persona de referència"),
        required=False)

    dexteritytextindexer.searchable('tipus_gestio')
    tipus_gestio = schema.TextLine(
        title=_(u"Tipus de gestió"),
        required=False)
