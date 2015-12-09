# -*- coding: utf-8 -*-
from zope import schema
from plone.directives import form
from plone.namedfile.field import NamedBlobFile

from genweb.ens import _


class ICarrec(form.Schema):
    """
    Càrrec associat a un òrgan d'un ens.
    """
    title = schema.TextLine(
        title=_(u"Nom"),
        required=True
    )

    description = schema.Text(
        title=_(u"Descripció"),
        required=False)

    persona = schema.TextLine(
        title=_(u"Persona"),
        required=True)

    data_nomenament = schema.Date(
        title=_(u"Data de nomenament"),
        required=True)

    document_nomenament = NamedBlobFile(
        title=_(u"Document de nomenament"),
        description=_(u"Puja un fitxer"),
        required=False)

    data_venciment = schema.Date(
        title=_(u"Data de venciment"),
        required=False)

    is_vigent = schema.Bool(
        title=_(u"Vigent"),
        required=False)

    observacions = schema.Text(
        title=_(u"Observacions"),
        required=False)

    is_directiu = schema.Bool(
        title=_(u"Directiu"),
        required=False)

    is_contacte = schema.Bool(
        title=_(u"Persona de contacte"),
        required=False)

    telefon = schema.TextLine(
        title=_(u"Telèfon"),
        required=False)

    email = schema.TextLine(
        title=_("Email"),
        required=False)
