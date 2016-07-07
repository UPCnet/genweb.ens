from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from genweb.ens.controlpanel import IEnsSettings
from genweb.ens.ws_client.indicators import Client


def get_settings_property(property_id):
    settings = getUtility(IRegistry).forInterface(IEnsSettings)
    return getattr(settings, property_id, None)


def get_ws_client():
    return Client(
        get_settings_property('ws_endpoint'), get_settings_property('ws_key'))

