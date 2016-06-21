# -*- coding: utf-8 -*-

from zope import schema
from plone.supermodel import model
from plone.app.registry.browser import controlpanel

from genweb.ens import _


class IEnsSettings(model.Schema):
    model.fieldset(
        'General',
        _(u'General'),
        fields=['url_info'])

    url_info = schema.TextLine(
        title=_(u"URL d'informació"),
        description=_(
            u"URL on enllaça la i de la barra superior del lloc web"),
        required=False)


class EnsSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IEnsSettings
    label = _(u'Paràmetres de configuració de Genweb Ens')

    def updateFields(self):
        super(EnsSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(EnsSettingsEditForm, self).updateWidgets()


class EnsSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = EnsSettingsEditForm
