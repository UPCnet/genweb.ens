# -*- coding: utf-8 -*-
from zope import schema
from plone.directives import form

from genweb.ens import _


class IPercentatgeParticipacio(form.Schema):
    """
    Percentatge de participació de la UPC en un ens.
    """

    title = schema.TextLine(
        title=_(u"Percentatge"),
        required=True
    )

    observacions = schema.Text(
        title=_(u"Observacions"),
        required=False)
