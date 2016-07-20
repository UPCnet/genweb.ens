from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from genweb.ens.controlpanel import IEnsSettings


def get_settings_property(property_id):
    settings = getUtility(IRegistry).forInterface(IEnsSettings)
    return getattr(settings, property_id, None)

