from five import grok
from plone.app.layout.viewlets.interfaces import IPortalHeader

from genweb.theme.browser.viewlets import gwHeader
from genweb.ens.interfaces import IGenwebEnsLayer
from genweb.ens.helpers import get_settings_property


class HeaderGWServeistic(gwHeader):
    grok.name('genweb.header')
    grok.viewletmanager(IPortalHeader)
    grok.template('header')
    grok.layer(IGenwebEnsLayer)

    def url_info(self):
        return get_settings_property('url_info') or ''
