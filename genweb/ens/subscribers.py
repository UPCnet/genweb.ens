from five import grok
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.CMFCore.utils import getToolByName

from genweb.ens.content.ens import IEns
from genweb.ens.indicators.updating import update as update_indicators


@grok.subscribe(IEns, IObjectRemovedEvent)
def update_indicators_on_deletion(obj, event):
    """
    Update indicators when a published ens has been deleted.
    """
    workflow_tool = getToolByName(obj, 'portal_workflow')
    if workflow_tool.getInfoFor(obj, 'review_state') in (
            'intranet', 'published'):
        update_indicators(context=obj)


@grok.subscribe(IEns, IActionSucceededEvent)
def update_indicators_on_review_state_change(obj, event):
    """
    Update indicators when the ens has been published/unpublished.
    """
    update_indicators(context=obj)

