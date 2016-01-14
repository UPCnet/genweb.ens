# -*- coding: utf-8 -*-

from datetime import datetime

from plone import api


def create_content(container, properties):
    content_dict = {'container': container}
    content_dict.update(properties)
    return api.content.create(**content_dict)

ens_1 = {
    'type': 'genweb.ens.ens',
    'id': 'amnistia-internacional',
    'title': u"Amnistía Internacional",
    'acronim': u"AI",
    'codi': u"11A",
    'nif': u"X82771235",
    'estat': u"Pre-alta cancel·lada",
    'figura_juridica': u"Fundació",
    'seu_social': u"Resta d'Espanya",
    'seu_social_stranger': None,
    'percentatge_participacio': 15.35,
    'aportacio_sn': True,
    'aportacio_import': 2300.50,
    'aportacio_moneda': u"€/any",
    'quota_sn': True,
    'quota_import': 253.44,
    'quota_moneda': u"€/mes",
    'web': u"www.amnistia.org"}

ens_2 = {
    'type': 'genweb.ens.ens',
    'id': 'green peace',
    'title': u"Green Peace",
    'acronim': u"Gp",
    'codi': u"22A",
    'nif': None,
    'estat': u"Pre-Baixa",
    'figura_juridica': u"Sense NIF",
    'seu_social': u"Estranger",
    'seu_social_estranger': u"Dublín",
    'percentatge_participacio': None,
    'aportacio_sn': False,
    'aportacio_import': None,
    'aportacio_moneda': None,
    'quota_sn': True,
    'quota_import': 253.44,
    'quota_moneda': None,
    'web': u"www.greenpeace.org"}

ens_incomplete = {
    'type': 'genweb.ens.ens',
    'id': 'amitges',
    'title': u"Amitges",
    'acronim': u"Amt"}

organ_1 = {
    'type': 'genweb.ens.organ',
    'id': 'consell-de-direccio',
    'title': u'Consell de Direcció',
    'tipus': 'Govern'}

carrec_1 = {
    'type': 'genweb.ens.carrec_upc',
    'id': 'colomina-pardo-otto',
    'title': u'Colomina Pardo, Ottö',
    'carrec': u"Membre excel·lent",
    'is_historic': False,
    'data_inici': datetime(2015, 2, 15)}

carrec_2 = {
    'type': 'genweb.ens.carrec_upc',
    'id': 'carmena-iglesias-ada',
    'title': u'Carmena Iglesias, Ada',
    'carrec': u"Vocal",
    'is_historic': True,
    'data_inici': datetime(2013, 12, 24)}
