# -*- coding: utf-8 -*-
from zope import schema

from genweb.ens import _
from genweb.ens.content.document_legal import IDocumentLegal


class IEscripturaPublica(IDocumentLegal):
    """
    Escriptura pública associada a un ens.
    """

    notari = schema.TextLine(
        title=_(u"Notari"),
        required=False,
    )
