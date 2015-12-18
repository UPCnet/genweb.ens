# -*- coding: utf-8 -*-
from zope import schema

from genweb.ens import _
from genweb.ens.content.document_legal import IDocumentLegal


class IEstatut(IDocumentLegal):
    """
    Estatut associat a un ens.
    """

    is_vigent = schema.Bool(
        title=_(u"Vigent"),
        defaultFactory=lambda: True,
        required=False,
    )
