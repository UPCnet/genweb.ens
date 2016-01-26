# -*- coding: utf-8 -*-

from plone import api


def create_content_kw(**properties):
    return api.content.create(**properties)


def create_carrec(container,
                  ens_num, organ_type, organ_num, carrec_num, persona_num,
                  is_historic=False):
    organ_type_code = organ_type.lower()[0]
    return create_content_kw(
        container=container,
        type='genweb.ens.carrec_upc',
        ens=u'UPC',
        title=u'Persona {0:02} - e{1:02}o{2}{3:02}c{4:02}{5}'.format(
            persona_num, ens_num, organ_type_code, organ_num, carrec_num,
            'h' if is_historic else ''),
        carrec=u'Càrrec {0:02}'.format(carrec_num),
        is_historic=is_historic)


def create_organ(container, organ_type, organ_num):
    return create_content_kw(
        container=container,
        type='genweb.ens.organ',
        title=u'Òrgan {0} {1:02}'.format(organ_type, organ_num),
        tipus=organ_type)


def create_ens(container, ens_num, **properties):
    return create_content_kw(
        container=container,
        type='genweb.ens.ens',
        title=u'Ens {0:02}'.format(ens_num),
        **properties)

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
