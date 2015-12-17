# -*- coding: utf-8 -*-

from zope import schema
from collective import dexteritytextindexer

from genweb.ens import _
from genweb.ens.content.persona import IPersona


class IPersonaContacte(IPersona):
    """
    Persona amb un càrrec i dades de contacte
    """

    dexteritytextindexer.searchable('telefon')
    telefon = schema.TextLine(
        title=_(u"Telèfon"),
        required=False
    )

    # TODO Validate email
    dexteritytextindexer.searchable('email')
    email = schema.TextLine(
        title=_(u"Email"),
        required=False
    )
