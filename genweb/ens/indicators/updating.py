# -*- coding: utf-8 -*-

import logging

from genweb.ens.helpers import get_ws_client
from genweb.ens.ws_client.indicators import ClientException
from genweb.ens.indicators.registry import get_indicators

logger = logging.getLogger(name='genweb.ens')


class Updater(object):
    def __init__(self, ws_client):
        self._ws_client = ws_client

    def _update_categories(self, indicator):
        for category in indicator.categories:
            self._ws_client.update_category(
                indicator.service, indicator.id,
                category.id, category.description, category.value)

    def update(self, indicator):
        try:
            self._update_categories(indicator)
            self._ws_client.update_indicator(
                indicator.service,
                indicator.id,
                indicator.description)
            updated = True
        except ClientException as e:
            logger.warning("WS client exception: {0}".format(e.message))
            updated = False
        return updated


def update(context):
    updater = Updater(get_ws_client())

    for indicator in get_indicators(context):
        if updater.update(indicator):
            logger.info(
                "Indicator '{0}' successfully updated".format(indicator.id))
        else:
            logger.warning(
                "Indicator '{0}' could not be updated".format(indicator.id))

