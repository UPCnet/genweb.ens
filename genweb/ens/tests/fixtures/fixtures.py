# -*- coding: utf-8 -*-

from datetime import datetime

from plone import api


class MockFile(object):
    def __init__(self, filename):
        self.filename = filename


def create_content(container, properties):
    content_dict = {'container': container}
    content_dict.update(properties)
    return api.content.create(**content_dict)

folder_1 = {
    'type': 'Folder',
    'id': 'folder-1',
    'title': 'Folder One'
}

folder_2 = {
    'type': 'Folder',
    'id': 'folder-2',
    'title': 'Folder Two'
}

ens_ai = {
    'type': 'genweb.ens.ens',
    'id': 'amnistia-internacional',
    'title': u"Amnistía Internacional",
    'description': u"ONG que defensa els drets humans arreu del món",
    'acronim': u"AI",
    'codi': u"11A",
    'nif': u"X82771235",
    'figura_juridica': u"Fundació",
    'numero_identificacio': u"12345A",
    'estat': u"Pre-alta cancel·lada",
    'domicili_social': u"Carrer Rosselló 99",
    'adreca_oficines_1': u"Avinguda Diagonal 123",
    'adreca_oficines_2': u"Carrer Gran de Sant Andreu 55 1r-1a",
    'telefon': u"698767762",
    'fax': u"987336536",
    'web': u"www.amnesty.org",
    'tipologia_upc': u"Participació Superior",
    'dades_identificatives_observacions': u"Participació recent",
    'aportacio_sn': True,
    'aportacio_import': 2300.50,
    'aportacio_moneda': u"€/any",
    'quota_sn': True,
    'quota_import': 253.44,
    'quota_moneda': u"€/mes",
    'unitat_carrec': u"Desconeguda",
    'percentatge_participacio': 15.35,
    'nombre_membres': u"2 de 10",
    'capital_social_sn': True,
    'capital_social_import': 2000,
    'capital_social_moneda': u"EUR",
    'participacio_observacions': u"No hi ha observacions que paguen la pena",
    'data_constitucio': datetime(2005, 2, 17),
    'entitats_constituents': u"Són varies",
    'entitats_actuals': u"Les mateixes",
    'data_entrada': datetime(2015, 3, 11),
    'data_entrada_descripcio': u"Va ser un gran dia",
    'seu_social': u"Resta d'Espanya",
    'seu_social_stranger': None,
    'adscripcio': u'Vallés oriental',
    'marc_legal_observacions': u"És un marc legal impecable"}

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
    'adscripcio': u"Vallés occidental",
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
    'adscripcio': u"Vallés oriental",
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

organ_2 = {
    'type': 'genweb.ens.organ',
    'id': 'patronat',
    'title': u'Patronat',
    'tipus': 'Govern'}

organ_3 = {
    'type': 'genweb.ens.organ',
    'id': 'administracio',
    'title': u'Administració',
    'tipus': 'Govern'}

organ_4 = {
    'type': 'genweb.ens.organ',
    'id': 'justicia',
    'title': u'Justícia',
    'tipus': 'Assessor'}

organ_5 = {
    'type': 'genweb.ens.organ',
    'id': 'investigacio',
    'title': u'Investigació',
    'tipus': 'Assessor'}

organ_6 = {
    'type': 'genweb.ens.organ',
    'id': 'Finances',
    'title': u'Finances',
    'tipus': 'Assessor'}

carrec_1 = {
    'type': 'genweb.ens.carrec_upc',
    'id': 'colomina-pardo-otto',
    'ens': u"UPC",
    'title': u'Colomina Pardo, Ottö',
    'carrec': u"Membre excel·lent",
    'data_inici': datetime(2015, 2, 15),
    'data_fi': datetime(2015, 8, 15),
    'is_historic': False}

carrec_2 = {
    'type': 'genweb.ens.carrec_upc',
    'id': 'carmena-iglesias-ada',
    'ens': u"UPC",
    'title': u'Carmena Iglesias, Ada',
    'carrec': u"Vocal",
    'data_inici': datetime(2013, 12, 24),
    'data_fi': datetime(2014, 11, 24),
    'is_historic': True}

carrec_3 = {
    'type': 'genweb.ens.carrec',
    'id': 'albaida-jordi',
    'ens': u"AB Seguros",
    'title': u'Albaida, Jordi',
    'carrec': u"Vocal",
    'data_inici': datetime(2011, 1, 4),
    'data_fi': None,
    'is_historic': False}

carrec_4 = {
    'type': 'genweb.ens.carrec',
    'id': 'zurito-marina',
    'ens': u"AB Seguros",
    'title': u'Zurito, Marina',
    'carrec': u"Adjunta",
    'data_inici': datetime(2012, 1, 4),
    'data_fi': None,
    'is_historic': False}

carrec_5 = {
    'type': 'genweb.ens.carrec',
    'id': 'hernando-simon',
    'ens': u"BBVA",
    'title': u'Hernado, Simón',
    'carrec': u"Vocal",
    'data_inici': None,
    'data_fi': None,
    'is_historic': True}

persona_directiu_1 = {
    'type': 'genweb.ens.persona_directiu',
    'id': 'solana-i-duran-albert',
    'title': 'Solana i Duran, Albert',
    'carrec': 'Subdirector',
    'telefon': '676998776',
    'email': 'solanaidura@amnesty.org',
}

persona_directiu_2 = {
    'type': 'genweb.ens.persona_directiu',
    'id': 'llopis-pascual-raul',
    'title': 'Llopis Pasqual, Raúl',
    'carrec': 'Gerent',
    'telefon': '656777987',
    'email': 'llopispascual@amnesty.org',
}

persona_contacte_1 = {
    'type': 'genweb.ens.persona_contacte',
    'id': 'medina-soler-andreu',
    'title': 'Medina Soler, Andreu',
    'carrec': 'Gerent',
    'telefon': '6789998991',
    'email': 'medinasoler@amnesty.org',
}

persona_contacte_2 = {
    'type': 'genweb.ens.persona_contacte',
    'id': 'hernandez-herrera-luisa',
    'title': 'Hernández Herrera, Luisa',
    'carrec': 'Presidenta',
    'telefon': '667556772',
    'email': 'hernandezherrera@amnesty.org',
}

unitat_1 = {
    'type': 'genweb.ens.unitat',
    'id': 'departament-de-ciencies',
    'title': 'Departament de ciències',
    'persona': 'Messeguer Muñoz, Àngela',
    'observacions': 'Cap'
}

unitat_2 = {
    'type': 'genweb.ens.unitat',
    'id': 'associacio-de-professorat',
    'title': 'Associació de professorat',
    'persona': 'Garcia Rico, David',
    'observacions': "És l'administrador"
}

acord_1 = {
    'type': 'genweb.ens.acord',
    'id': 'primer-acord',
    'title': 'Primer acord',
    'description': "És el primer acord",
    'data': datetime(2015, 1, 5),
    'fitxer': MockFile('acord_1.pdf'),
    'organ': 'Patronat'
}

acord_2 = {
    'type': 'genweb.ens.acord',
    'id': 'segon-acord',
    'title': 'Segon acord',
    'description': "És el segon acord",
    'data': datetime(2015, 1, 3),
    'fitxer': None,
    'organ': 'Yoga'
}

acord_3 = {
    'type': 'genweb.ens.acord',
    'id': 'tercer-acord',
    'title': 'Tercer acord',
    'description': "És el tercer acord",
    'data': None,
    'fitxer': MockFile('acord_3.pdf'),
    'organ': 'Administració'
}

acord_4 = {
    'type': 'genweb.ens.acord',
    'id': 'quart-acord',
    'title': 'Quart acord',
    'description': "És el quart acord",
    'data': datetime(2015, 1, 4),
    'fitxer': MockFile('acord_4.pdf'),
    'organ': 'Administració'
}

escriptura_1 = {
    'type': 'genweb.ens.escriptura_publica',
    'id': 'primera-escriptura',
    'title': 'Primera escriptura',
    'description': "És la primera escriptura",
    'data': datetime(2012, 5, 25),
    'fitxer': MockFile('escriptura_1.pdf'),
    'notari': 'Asensi Llopis, Neus'
}

escriptura_2 = {
    'type': 'genweb.ens.escriptura_publica',
    'id': 'segona-escriptura',
    'title': 'Segona escriptura',
    'description': "És la segona escriptura",
    'data': datetime(2012, 5, 24),
    'fitxer': None,
    'notari': 'Filiu Torrent, Eli'
}

escriptura_3 = {
    'type': 'genweb.ens.escriptura_publica',
    'id': 'tercera-escriptura',
    'title': 'Tercera escriptura',
    'description': "És la tercera escriptura",
    'data': None,
    'fitxer': MockFile('escriptura_3.pdf'),
    'notari': None
}

escriptura_4 = {
    'type': 'genweb.ens.escriptura_publica',
    'id': 'quarta-escriptura',
    'title': 'Quarta escriptura',
    'description': "És la quarta escriptura",
    'data': datetime(2012, 5, 26),
    'fitxer': MockFile('escriptura_4.pdf'),
    'notari': 'Salinas Martorell, Héctor'
}

estatut_1 = {
    'type': 'genweb.ens.estatut',
    'id': 'primer-estatut',
    'title': 'Primer estatut',
    'description': "És el primer estatut",
    'data': None,
    'fitxer': MockFile('estatut_1.pdf'),
    'is_vigent': True
}

estatut_2 = {
    'type': 'genweb.ens.estatut',
    'id': 'segon-estatut',
    'title': 'Segon estatut',
    'description': "És el segon estatut",
    'data': datetime(2002, 11, 23),
    'fitxer': MockFile('estatut_2.pdf'),
    'is_vigent': True
}

estatut_3 = {
    'type': 'genweb.ens.estatut',
    'id': 'tercer-estatut',
    'title': 'Tercer estatut',
    'description': "És el tercer estatut",
    'data': datetime(2002, 11, 22),
    'fitxer': None,
    'is_vigent': True
}

estatut_4 = {
    'type': 'genweb.ens.estatut',
    'id': 'quart-estatut',
    'title': 'Quart estatut',
    'description': "És el quart estatut",
    'data': datetime(2003, 11, 24),
    'fitxer': MockFile('estatut_4.pdf'),
    'is_vigent': False
}

estatut_5 = {
    'type': 'genweb.ens.estatut',
    'id': 'cinque-estatut',
    'title': 'Cinquè estatut',
    'description': "És el cinquè estatut",
    'data': None,
    'fitxer': None,
    'is_vigent': False
}

estatut_6 = {
    'type': 'genweb.ens.estatut',
    'id': 'sise-estatut',
    'title': 'Sisè estatut',
    'description': "És el sisè estatut",
    'data': datetime(2003, 11, 23),
    'fitxer': MockFile('estatut_6.pdf'),
    'is_vigent': False
}

acta_1 = {
    'type': 'genweb.ens.acta_reunio',
    'id': 'acta-a',
    'title': 'Acta A',
    'description': "És la A",
    'data': datetime(2001, 4, 23),
    'fitxer': MockFile('acta_1.pdf')
}

acta_2 = {
    'type': 'genweb.ens.acta_reunio',
    'id': 'acta-b',
    'title': 'Acta B',
    'description': "És la B",
    'data': datetime(2001, 4, 24),
    'fitxer': None
}

acta_3 = {
    'type': 'genweb.ens.acta_reunio',
    'id': 'acta-c',
    'title': 'Acta C',
    'description': "És la C",
    'data': None,
    'fitxer': MockFile('acta_3.pdf')
}

conveni_1 = {
    'type': 'genweb.ens.conveni',
    'id': 'conveni-primer',
    'title': 'Primer conveni',
    'description': "És el primer",
    'data': datetime(2010, 9, 2),
    'fitxer': None
}

conveni_2 = {
    'type': 'genweb.ens.conveni',
    'id': 'conveni-segon',
    'title': 'Segon conveni',
    'description': "És el segon",
    'data': None,
    'fitxer': MockFile('conveni_2.pdf')
}

conveni_3 = {
    'type': 'genweb.ens.conveni',
    'id': 'conveni-tercer',
    'title': 'Tercer conveni',
    'description': "És el tercer",
    'data': datetime(2010, 9, 3),
    'fitxer': MockFile('conveni_3.pdf')
}

document_1 = {
    'type': 'genweb.ens.document_interes',
    'id': 'document-primer',
    'title': 'Primer document',
    'description': "És el primer",
    'data': None,
    'fitxer': MockFile('document_1.pdf')
}

document_2 = {
    'type': 'genweb.ens.document_interes',
    'id': 'document-segon',
    'title': 'Segon document',
    'description': "És el segon",
    'data': datetime(2013, 4, 12),
    'fitxer': MockFile('document_2.pdf')
}

document_3 = {
    'type': 'genweb.ens.document_interes',
    'id': 'document-tercer',
    'title': 'Tercer document',
    'description': "És el tercer",
    'data': datetime(2013, 4, 11),
    'fitxer': None
}

representant_1 = {
    'type': 'genweb.ens.representant',
    'id': 'jose-vicente-osorio',
    'title': u'José Vicente Osorio',
    'carrec': u'Vicerrector de Música'
}

representant_1_bis = {
    'type': 'genweb.ens.representant',
    'id': 'jose-vicente-osorio',
    'title': u'José Vicente Osorio',
    'carrec': u'Vicerrector de Concerts'
}

folder_consell_direccio = {
    'type': 'Folder',
    'id': 'consell-de-direccio',
    'title': u'Consell de direcció'
}

folder_altres = {
    'type': 'Folder',
    'id': 'altres',
    'title': u'Altres'
}
