import logging

import transaction
from Products.CMFCore.utils import getToolByName

from genweb.ens.helpers import get_settings_property
from genweb.core.indicators import RegistryException
from genweb.core.indicators import WebServiceReporter, ReporterException
from genweb.ens.indicators.registry import get_registry

logger = logging.getLogger(name='genweb.ens')


def update_if_review_state(content, review_state):
    workflow_tool = getToolByName(content, 'portal_workflow')
    if workflow_tool.getInfoFor(content, 'review_state') in review_state:
        update(context=content)


def update(context):
    transaction.get().addAfterCommitHook(
        update_after_commit_hook,
        kws=dict(context=context))


def update_after_commit_hook(is_commit_successful, context):
    if not is_commit_successful:
        return
    try:
        ws_url = get_settings_property('ws_endpoint')
        ws_key = get_settings_property('ws_key')
        registry = get_registry(context)

        reporter = WebServiceReporter(ws_url, ws_key)
        reporter.report(registry)
        logger.info("Indicators were successfully reported")
    except RegistryException as e:
        logger.warning(
            "Error while loading indicator registry ({0})".format(e))
    except ReporterException as e:
        logger.warning("Error while reporting indicators ({0})".format(e))

