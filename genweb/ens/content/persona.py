# -*- coding: utf-8 -*-

from plone.directives import form
from zope import schema
from collective import dexteritytextindexer

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

    dexteritytextindexer.searchable('carrec')
    carrec_envirtud = schema.TextLine(
        title=_(u"Com a..."),
        required=True
    )

    dexteritytextindexer.searchable('carrec')
    carrec = schema.TextLine(
        title=_(u"Càrrec a l'entitat"),
        required=True
    )
