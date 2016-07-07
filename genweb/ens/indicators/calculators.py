from Products.CMFCore.utils import getToolByName

from genweb.ens.data_access.ens import EnsDataReporter
from genweb.ens.indicators.beans import CategoryCalculator


class EnsNumber(CategoryCalculator):
    def __init__(self, context, contenidor):
        super(EnsNumber, self).__init__()
        self._context = context
        self._contenidor = contenidor

    def calculate(self):
        catalog = getToolByName(self._context, 'portal_catalog')
        reporter = EnsDataReporter(catalog)
        return len(reporter.list_by_contenidor_id_and_review_state(
            self._contenidor, ('intranet', 'published')))


class EnsNumberEstat(CategoryCalculator):
    def __init__(self, context, contenidor, estat):
        super(EnsNumberEstat, self).__init__()
        self._context = context
        self._contenidor = contenidor
        self._estat = estat

    def calculate(self):
        catalog = getToolByName(self._context, 'portal_catalog')
        reporter = EnsDataReporter(catalog)
        return len(reporter.list_by_contenidor_id_and_estat_and_review_state(
            self._contenidor, self._estat, ('intranet', 'published')))


class EnsNumberDelta(CategoryCalculator):
    def __init__(self, context, contenidor, delta):
        super(EnsNumberDelta, self).__init__()
        self._context = context
        self._contenidor = contenidor
        self._delta = delta

    def calculate(self):
        catalog = getToolByName(self._context, 'portal_catalog')
        reporter = EnsDataReporter(catalog)
        return len(reporter.list_by_contenidor_id_and_delta_and_review_state(
            self._contenidor, self._delta, ('intranet', 'published')))

