# -*- coding: utf-8 -*-

from zope import schema

from genweb.ens import _
from genweb.ens.content.persona_contacte import IPersonaContacte


class IPersonaDirectiu(IPersonaContacte):
    is_historic = schema.Bool(
        title=_(u"Històric"),
        defaultFactory=lambda: False,
        required=False)
