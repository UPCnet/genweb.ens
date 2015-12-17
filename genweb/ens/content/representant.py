# -*- coding: utf-8 -*-

from zope import schema

from genweb.ens import _
from genweb.ens.content.persona import IPersona


class IRepresentant(IPersona):
    """
    Càrrec que pot representar UPC en algun ens
    """

    is_consell_direccio = schema.Bool(
        title=_(u"Forma part del Consell de Direcció"),
        required=False)
