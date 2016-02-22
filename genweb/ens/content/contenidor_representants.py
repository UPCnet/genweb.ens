# -*- coding: utf-8 -*-

from zope import schema
from collective import dexteritytextindexer
from plone.directives import form

from genweb.ens import _


class IContenidorRepresentants(form.Schema):
    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Nom"),
        required=True)

    dexteritytextindexer.searchable('description')
    description = schema.Text(
        title=_(u"Descripció"),
        required=False)
