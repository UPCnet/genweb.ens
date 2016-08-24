from five import grok
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from Products.CMFCore.interfaces import IActionSucceededEvent

from genweb.ens.content.ens import IEns
from genweb.ens.indicators.updating import (
    update as update_indicators,
    update_if_review_state as update_indicators_if_review_state)


@grok.subscribe(IEns, IObjectRemovedEvent)
def update_indicators_on_ens_deletion(obj, event):
    update_indicators_if_review_state(obj, ('intranet', 'published'))


@grok.subscribe(IEns, IActionSucceededEvent)
def update_indicators_on_ens_review_state_change(obj, event):
    update_indicators(context=obj)
