# -*- coding: utf-8 -*-
from zope import schema
from plone.directives import form
from plone.namedfile.field import NamedBlobFile

from genweb.ens import _


class IConveni(form.Schema):
    """
    Conveni legal d'interès
    """

    title = schema.TextLine(
        title=_(u"Descripció"),
        required=True)

    data = schema.Date(
        title=_(u"Data"),
        required=False)

    fitxer = NamedBlobFile(
        title=_(u"Fitxer"),
        description=_(u"Puja un fitxer"),
        required=True)
