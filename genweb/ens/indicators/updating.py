import logging

from genweb.ens.helpers import get_settings_property
from genweb.core.indicators import RegistryException
from genweb.core.indicators import WebServiceReporter, ReporterException
from genweb.ens.indicators.registry import get_registry

logger = logging.getLogger(name='genweb.ens')


def update(context):
    try:
        registry = get_registry(context)
        ws_url = get_settings_property('ws_endpoint')
        ws_key = get_settings_property('ws_key')
        reporter = WebServiceReporter(ws_url, ws_key)
        reporter.report(registry)
        logger.info("Indicators were successfully reported")
    except RegistryException as e:
        logger.warning(
            "Error while loading indicator registry ({0})".format(e))
    except ReporterException as e:
        logger.warning("Error while reporting indicators ({0})".format(e))

