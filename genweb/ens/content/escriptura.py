# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import implements
from plone.directives import form
from plone.dexterity.content import Item
from plone.namedfile.field import NamedBlobFile

from genweb.ens import _


class IEscriptura(form.Schema):
    """
    Escriptura pública associada a un ens.
    """

    title = schema.TextLine(
        title=_(u"Descripció"),
        required=True
    )

    data = schema.Date(
        title=_(u"Data"),
        required=False)

    notari = schema.TextLine(
        title=_(u"Notari"),
        required=False,
    )

    fitxer = NamedBlobFile(
        title=_(u"Fitxer"),
        description=_(u"Puja un fitxer"),
        required=True,
    )


class Escriptura(Item):
    implements(IEscriptura)
