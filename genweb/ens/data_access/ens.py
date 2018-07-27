# -*- coding: utf-8 -*-
import datetime
from DateTime import DateTime

from genweb.ens.content.ens import (get_denominacio,
                                    get_percentatge_membres,
                                    get_percentatge_participacio,
                                    get_aportacio, get_quota)


class EnsSearchResult(object):
    def __init__(self, title, acronim, url):
        self.title = title
        self.acronim = acronim
        self.url = url


class Identificacio(object):
    def __init__(self, codi, num_ens, acronim, title, absolute_url, nif, numero_identificacio, estat, institution_type,
                 figura_juridica, seu_social, seu_social_estranger, adscripcio, percentatge_participacio, nombre_membres,
                 aportacio, quota, tags, etiquetes, web, tipologia_upc, entitats_actuals):
        self.codi = codi
        self.num_ens = num_ens
        self.acronim = acronim
        self.title = title
        self.absolute_url = absolute_url
        self.nif = nif
        self.numero_identificacio = numero_identificacio
        self.estat = estat
        self.institution_type = institution_type
        self.figura_juridica = figura_juridica
        self.seu_social = seu_social
        self.seu_social_estranger = seu_social_estranger
        self.adscripcio = adscripcio
        self.percentatge_participacio = percentatge_participacio
        self.nombre_membres = nombre_membres
        self.aportacio = aportacio
        self.quota = quota
        self.tags = tags
        self.etiquetes = etiquetes
        self.web = web
        self.tipologia_upc = tipologia_upc
        self.entitats_actuals = entitats_actuals


class Representacio(object):
    def __init__(self, denominacio, absolute_url, organ, carrec, persona, carrec_envirtud,
                 data_nomenament):
        self.denominacio = denominacio
        self.absolute_url = absolute_url
        self.organ = organ
        self.carrec = carrec
        self.persona = persona
        self.carrec_envirtud = carrec_envirtud
        self.data_nomenament = data_nomenament


def get_sortable_key_by_date(obj):
    """
    Given an object A with a 'data' property with type datetime.date,
    returns a string that can be used to compare A with B, so that
    A < B is true when A.data is older than B.data. If data is None, then
    the oldest possible date is considered.
    """
    return (obj.data and obj.data.strftime('%Y%m%d') or
            datetime.datetime(1900, 1, 1).strftime('%Y%m%d'))


class EnsDataReporter(object):
    def __init__(self, catalog):
        self.catalog = catalog

    def get_path(self, obj):
        """
        Return a Plone object's path tentatively.
        """
        if 'getPath' in dir(obj):
            return obj.getPath()
        elif 'getPhysicalPath' in dir(obj):
            return '/'.join(obj.getPhysicalPath())
        else:
            return None

    def list(self, search_filters=None):
        """
        List ens.
        """
        query = {
            'portal_type': 'genweb.ens.ens',
            'sort_on': 'sortable_title'
        }
        if search_filters:
            query.update(search_filters)
        return self.catalog.searchResults(query)

    def list_by_contenidor_id_and_review_state(
            self, contenidor_id, review_state=None):
        ens = []
        contenidor = self.list_contenidor_by_id(contenidor_id)
        if contenidor:
            filters = dict(
                portal_type='genweb.ens.ens',
                path={'query': contenidor.getPath()},
                sort_on='sortable_title')
            if review_state:
                filters['review_state'] = review_state
            ens = self.catalog.searchResults(filters)
        return ens

    def list_by_contenidor_id_and_estat_and_review_state(
            self, contenidor_id, estat, review_state=None):
        ens = []
        contenidor = self.list_contenidor_by_id(contenidor_id)
        if contenidor:
            filters = dict(
                portal_type='genweb.ens.ens',
                estat=estat,
                path={'query': contenidor.getPath()},
                sort_on='sortable_title')
            if review_state:
                filters['review_state'] = review_state
            ens = self.catalog.searchResults(filters)
        return ens

    def _datetime_to_DateTime(self, obj):
        return DateTime(
            obj.year, obj.month, obj.day,
            obj.hour, obj.minute, obj.second)

    def _get_date_range(self, delta, date_source=None):
        """
        Get a list representing the range of dates between now and now + delta.
        :param delta: Number of days behind/ahead the source date. If < 0,
        range is [source + delta, source], else [source, source + delta]
        :param date_source: datetime.datetime to which delta is applied.
        :return: 2-DateTime.DateTime element list representing the date range.
        """
        date_now = date_source if date_source else datetime.datetime.now()
        date_delta = date_now + datetime.timedelta(days=delta)
        datetime_now = self._datetime_to_DateTime(date_now)
        datetime_delta = self._datetime_to_DateTime(date_delta)
        return sorted([datetime_now, datetime_delta])

    def list_by_contenidor_id_and_delta_and_review_state(
            self, contenidor_id, delta, review_state=None, date_source=None):
        ens = []
        contenidor = self.list_contenidor_by_id(contenidor_id)
        if contenidor:
            filters = dict(
                portal_type='genweb.ens.ens',
                effective={
                    'query': self._get_date_range(delta, date_source),
                    'range': 'min:max'},
                path={'query': contenidor.getPath()},
                sort_on='sortable_title')
            if review_state:
                filters['review_state'] = review_state
            ens = self.catalog.searchResults(filters)
        return ens

    def list_contenidor_by_id(self, contenidor_id):
        contenidor = None
        contenidors = self.catalog.searchResults(
            portal_type='genweb.ens.contenidor_ens',
            id=contenidor_id,
            sort_on='sortable_title')
        if contenidors:
            contenidor = contenidors[0]
        return contenidor

    def list_unitats_by_ens_obj(self, ens):
        return [unitat.getObject() for unitat in self.catalog.searchResults(
            portal_type='genweb.ens.unitat',
            sort_on='sortable_title',
            path={
                'query': self.get_path(ens),
                'depth': 1
            })]

    def list_acords_by_ens_obj(self, ens):
        """
        List acord(s) related to the specified ens.
        """
        return sorted(
            [acord.getObject() for acord in self.catalog.searchResults(
                portal_type='genweb.ens.acord',
                path={
                    'query': self.get_path(ens),
                    'depth': 1
                })],
            key=get_sortable_key_by_date, reverse=True)

    def list_escriptures_by_ens_obj(self, ens):
        return sorted([
            escript.getObject() for escript in self.catalog.searchResults(
                portal_type='genweb.ens.escriptura_publica',
                path={
                    'query': self.get_path(ens),
                    'depth': 1
                })],
            key=get_sortable_key_by_date, reverse=True)

    def list_estatuts_by_ens_obj(self, ens, is_vigent=True):
        # TODO Optimise this code so that the sorting is performed by ZODB
        return sorted([
            estatut.getObject() for estatut in self.catalog.searchResults(
                portal_type='genweb.ens.estatut',
                is_vigent=is_vigent,
                path={
                    'query': self.get_path(ens),
                    'depth': 1
                })],
            key=get_sortable_key_by_date, reverse=True)

    def list_actes_reunio_by_ens_obj(self, ens):
        return sorted([acta.getObject() for acta in self.catalog.searchResults(
            portal_type='genweb.ens.acta_reunio',
            path={
                'query': self.get_path(ens),
                'depth': 1
            })],
            key=get_sortable_key_by_date, reverse=True)

    def list_convenis_by_ens_obj(self, ens):
        return sorted(
            [conveni.getObject() for conveni in self.catalog.searchResults(
                portal_type='genweb.ens.conveni',
                path={
                    'query': self.get_path(ens),
                    'depth': 1
                })],
            key=get_sortable_key_by_date, reverse=True)

    def list_documents_interes_by_ens_obj(self, ens):
        return sorted([doc.getObject() for doc in self.catalog.searchResults(
            portal_type='genweb.ens.document_interes',
            path={
                'query': self.get_path(ens),
                'depth': 1
            })],
            key=get_sortable_key_by_date, reverse=True)

    def list_organs_by_ens(self, ens, tipus=None):
        """
        List organ(s) related to the specified ens.
        """
        query = {
            'portal_type': 'genweb.ens.organ',
            'sort_on': 'getObjPositionInParent',
            'path': {
                'query': self.get_path(ens),
                'depth': 1
            }
        }
        if tipus:
            query['tipus'] = tipus
        return self.catalog.searchResults(query)

    def list_directius_by_ens_obj(self, ens):
        return [carrec.getObject() for carrec in self.catalog.searchResults(
            portal_type='genweb.ens.persona_directiu',
            sort_on='sortable_title',
            path={
                'query': self.get_path(ens),
                'depth': 1
            })]

    def list_contactes_by_ens_obj(self, ens):
        return [carrec.getObject() for carrec in self.catalog.searchResults(
            portal_type='genweb.ens.persona_contacte',
            sort_on='sortable_title',
            path={
                'query': self.get_path(ens),
                'depth': 1
            })]

    def list_carrecs_upc_by_organ(self, organ, is_historic=None):
        """
        List carrec_upc(s) related to the specified ens' organ.
        """
        query = {
            'portal_type': 'genweb.ens.carrec_upc',
            'path': {
                'query': self.get_path(organ),
                'depth': 1
            }
        }
        if is_historic is not None:
            query['is_historic'] = is_historic

        return sorted(self.catalog.searchResults(query),
                      key=lambda e: (e.carrec + e.Title.decode('utf-8')))

    def list_carrecs_by_organ_grouped_by_ens_obj(self, organ,
                                                 is_historic=None):
        """
        List all the carrec_upc(s) and carrec(s) related to the specified ens'
        organ, grouped by the carrec's ens. Return a list of tuples, each
        having two elements:
        - 0: carrec's ens title,
        - 1: list of carrec(s) related to the ens at index 0.
        The tuples of the list are sorted as follows:
        - (1st) ens is "UPC",
        - (2nd) alphabetically by ens title,
        - (3rd) alphabetically by carrec title.
        """
        carrecs_by_organ = []
        query = {
            'portal_type': 'genweb.ens.carrec_upc',
            'sort_on': 'carrec',
            'path': {
                'query': organ.getPath(),
                'depth': 1
            }}
        if is_historic is not None:
            query['is_historic'] = is_historic

        # Retrieve UPC carrecs
        carrecs_upc = [carrec.getObject()
                       for carrec in self.catalog.searchResults(query)]
        if carrecs_upc:
            carrecs_by_organ.append(("UPC", carrecs_upc))

        # Retrieve non-UPC carrecs
        query['portal_type'] = 'genweb.ens.carrec'
        carrecs_by_ens = {}
        for carrec in self.catalog.searchResults(query):
            carrec_obj = carrec.getObject()
            if carrec_obj.ens not in carrecs_by_ens:
                carrecs_by_ens[carrec_obj.ens] = []
            carrecs_by_ens[carrec_obj.ens].append(carrec_obj)

        # Append non-UPC carrecs grouped by their alphabetically sorted ens
        for ens, carrecs in sorted(
                carrecs_by_ens.iteritems(), key=lambda e: e[0].lower()):
            carrecs_by_organ.append((ens, carrecs))

        return carrecs_by_organ

    def list_identificacio(self, search_filters=None):
        """
        List all the ens(s)' identification info.
        """
        identificacio = []
        for ens in self.list(search_filters):
            ens_obj = ens.getObject()
            identificacio.append(Identificacio(
                codi=ens_obj.codi or "-",
                num_ens=ens_obj.num_ens or "-",
                acronim=ens_obj.acronim or "-",
                title=ens_obj.title or "-",
                absolute_url=ens_obj.absolute_url,
                nif=ens_obj.nif or "-",
                numero_identificacio=ens_obj.numero_identificacio or "-",
                estat=ens_obj.estat or "-",
                institution_type=ens_obj.institution_type or "-",
                figura_juridica=ens_obj.figura_juridica or "-",
                seu_social=ens_obj.seu_social or "-",
                seu_social_estranger=ens_obj.seu_social_estranger or "-",
                adscripcio=ens_obj.adscripcio or "-",
                percentatge_participacio=get_percentatge_participacio(ens_obj),
                nombre_membres=ens_obj.nombre_membres or "-",
                percentatge_membres=get_percentatge_membres(ens_obj),
                aportacio=get_aportacio(ens_obj),
                quota=get_quota(ens_obj),
                tags=ens_obj.Subject,
                etiquetes=ens_obj.etiquetes or "-",
                web=ens_obj.web or "-",
                tipologia_upc=ens_obj.tipologia_upc or "-",
                entitats_actuals=ens_obj.entitats_actuals or "-"))
        return identificacio

    def list_representacio(self, is_historic=None, search_filters=None):
        """
        List all the ens(s) along with the carrec_upc(s) related to their
        organs, only for those ens(s) having at least one carrec_upc
        associated. Return a list of Representacio objects where the elements
        are sorted alphabetically by (1st) ens.title, (2nd) organ.title and
        (3rd) carrec.carrec.
        """
        representacio = []
        for ens in self.list(search_filters):
            ens_obj = ens.getObject()
            ens_estat = ens_obj.estat
            if ens_estat in ('Actiu', 'Pre-Baixa'):
                for organ_tipus in ('Govern', 'Assessor'):
                    for organ in self.list_organs_by_ens(ens, organ_tipus):
                        for carrec in self.list_carrecs_upc_by_organ(organ, False):
                            carrec_obj = carrec.getObject()
                            representacio.append(Representacio(
                                denominacio=get_denominacio(ens_obj),
                                absolute_url=ens_obj.absolute_url,
                                organ=organ.Title.decode('utf-8'),
                                carrec=carrec_obj.carrec,
                                persona=carrec_obj.title,
                                carrec_envirtud=carrec_obj.carrec_envirtud or "-",
                                data_nomenament=carrec_obj.data_inici and
                                carrec_obj.data_inici.strftime('%d/%m/%Y') or "-"))
        return representacio

    def search(self, search_filters=None):
        query = {'portal_type': 'genweb.ens.ens', 'sort_on': 'sortable_title'}
        if search_filters:
            query.update(search_filters)

        return [EnsSearchResult(
            title=ens.Title,
            acronim=ens.acronim,
            url=ens.getURL()) for ens in self.catalog.searchResults(query)]
