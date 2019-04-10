# -*- coding: utf-8 -*-

from collective import dexteritytextindexer
from five import grok
from plone.directives import form
from plone.indexer import indexer
from zope import schema

from genweb.ens import _


class IPersona(form.Schema):
    """
    Persona amb un càrrec
    """

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Cognoms i nom"),
        description=_(u"Escriu amb el format: Cognoms, Nom"),
        required=True
    )

    dexteritytextindexer.searchable('dni')
    dni = schema.TextLine(
        title=_(u"DNI"),
        required=False)

    dexteritytextindexer.searchable('carrec')
    carrec = schema.TextLine(
        title=_(u"Carrec"),
        required=False
    )
