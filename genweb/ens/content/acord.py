# -*- coding: utf-8 -*-
from zope import schema
from collective import dexteritytextindexer

from genweb.ens.content.document_legal import IDocumentLegal
from genweb.ens import _


class IAcord(IDocumentLegal):
    """
    Acord legal associt a un òrgan de govern.
    """
    dexteritytextindexer.searchable('organ')
    organ = schema.TextLine(
        title=_(u"Òrgan"),
        required=False
    )
