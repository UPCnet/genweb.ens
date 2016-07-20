from Products.CMFCore.utils import getToolByName

from genweb.ens.data_access.ens import EnsDataReporter
from genweb.core.indicators import Calculator


class EnsNumber(Calculator):
    def calculate(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        reporter = EnsDataReporter(catalog)
        return len(reporter.list_by_contenidor_id_and_review_state(
            self.category.id, ('intranet', 'published')))


class EnsNumberEstat(Calculator):
    def __init__(self, context, estat):
        super(EnsNumberEstat, self).__init__(context)
        self._estat = estat

    def calculate(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        reporter = EnsDataReporter(catalog)
        return len(reporter.list_by_contenidor_id_and_estat_and_review_state(
            self.category.id, self._estat, ('intranet', 'published')))


class EnsNumberEstatActiu(EnsNumberEstat):
    def __init__(self, context):
        super(EnsNumberEstatActiu, self).__init__(context, "Actiu")


class EnsNumberEstatBaixa(EnsNumberEstat):
    def __init__(self, context):
        super(EnsNumberEstatBaixa, self).__init__(context, "Baixa")


class EnsNumberDelta(Calculator):
    def __init__(self, context, delta):
        super(EnsNumberDelta, self).__init__(context)
        self._delta = delta

    def calculate(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        reporter = EnsDataReporter(catalog)
        return len(reporter.list_by_contenidor_id_and_delta_and_review_state(
            self.category.id, self._delta, ('intranet', 'published')))


class EnsNumberDeltaMonth(EnsNumberDelta):
    def __init__(self, context):
        super(EnsNumberDeltaMonth, self).__init__(context, -30)

