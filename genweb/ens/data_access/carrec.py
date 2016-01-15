# -*- coding: utf-8 -*-


class CarrecSearchResult(object):
    def __init__(self, title, ens, ens_url, organ, organ_url, carrec,
                 data_inici, data_inici_str, data_fi, data_fi_str,
                 is_historic, url):
        self.title = title
        self.ens = ens
        self.ens_url = ens_url
        self.organ = organ
        self.organ_url = organ_url
        self.carrec = carrec
        self.data_inici = data_inici
        self.data_inici_str = data_inici_str
        self.data_fi = data_fi
        self.data_fi_str = data_fi_str
        self.is_historic = is_historic
        self.url = url

    @property
    def sortable_key(self):
        return self.title + (
            self.data_inici and
            self.data_inici.strftime('%Y%m%d') or
            '99999999')


class CarrecDataReporter(object):
    def __init__(self, catalog):
        self.catalog = catalog

    def search(self, searchFilters=None):
        results = []

        query = {
            'portal_type': ('genweb.ens.carrec', 'genweb.ens.carrec_upc'),
            'sort_on': 'sortable_title'}
        if searchFilters:
            query.update(searchFilters)

        for carrec in self.catalog.searchResults(query):
            carrec_obj = carrec.getObject()
            ens = carrec_obj.getParentNode().getParentNode()
            organ = carrec_obj.getParentNode()
            results.append(CarrecSearchResult(
                title=carrec_obj.title,
                ens=ens.acronim,
                ens_url=ens.absolute_url,
                organ=organ.title,
                organ_url=organ.absolute_url,
                carrec=carrec_obj.carrec or "-",
                data_inici_str=(carrec_obj.data_inici and
                                carrec_obj.data_inici.strftime('%d/%m/%Y') or
                                '-'),
                data_inici=carrec_obj.data_inici,
                data_fi=carrec_obj.data_fi,
                data_fi_str=(carrec_obj.data_fi and
                             carrec_obj.data_fi.strftime('%d/%m/%Y') or
                             '-'),
                is_historic=carrec_obj.is_historic,
                url=carrec_obj.absolute_url))

        return sorted(results, key=lambda e: e.sortable_key)