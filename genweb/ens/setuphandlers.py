# -*- coding: utf-8 -*-

import os
import csv

from zope.component import getUtility
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes


data_folder_name = 'data'
consell_direccio_file_name = 'consell_direccio.csv'
fields_to_index = [('estat', 'FieldIndex'),
                   ('figura_juridica', 'FieldIndex'),
                   ('carrec', 'FieldIndex'),
                   ('is_historic', 'FieldIndex'),
                   ('data', 'DateIndex'),
                   ('is_vigent', 'FieldIndex'),
                   ('organ', 'FieldIndex'),
                   ('tipus', 'FieldIndex')]


def add_catalog_indexes(catalog):
    indexables = []
    indexes = catalog.indexes()
    for name, meta_type in fields_to_index:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
        if len(indexables) > 0:
            catalog.manage_reindexIndex(ids=indexables)


def add_container(container, type, title,
                  allowed_types=None, exclude_from_nav=False):
    folder_id = getUtility(IIDNormalizer).normalize(title)
    if folder_id not in container:
        folder = api.content.create(
            type=type,
            id=folder_id,
            title=title,
            container=container)
        api.content.transition(
            obj=folder,
            transition='reject')
        if allowed_types:
            behavior = ISelectableConstrainTypes(folder)
            behavior.setConstrainTypesMode(1)
            behavior.setLocallyAllowedTypes(allowed_types)
            behavior.setImmediatelyAddableTypes(allowed_types)
        folder.exclude_from_nav = exclude_from_nav
    return container[folder_id]


def add_representant_upc(folder, title, carrec):
    representant_id = getUtility(IIDNormalizer).normalize(title)
    if representant_id not in folder:
        representant = api.content.create(
            type='genweb.ens.representant',
            id=representant_id,
            title=title,
            container=folder,
            carrec=carrec)
        api.content.transition(
            obj=representant,
            transition='reject')
    return folder[representant_id]


def add_representants_upc():
    portal = api.portal.get()
    if 'ca' in portal:
        representants_folder = add_container(
            container=portal['ca'],
            type='Folder',
            title=u"Representants UPC",
            exclude_from_nav=True)
        consell_direccio_folder = add_container(
            container=representants_folder,
            type='genweb.ens.contenidor_representants',
            title=u"Consell de Direcció")
        add_container(
            container=representants_folder,
            type='genweb.ens.contenidor_representants',
            title=u"Altres")

        consell_direccio_file_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            data_folder_name,
            consell_direccio_file_name)

        with open(consell_direccio_file_path, 'r') as consell_direccio_file:
            for row in csv.reader(consell_direccio_file,
                                  delimiter=',', quotechar='"'):
                add_representant_upc(
                    consell_direccio_folder,
                    title=row[1].decode('utf-8'),
                    carrec=row[0].decode('utf-8'))


def add_collections_folder():
    portal = api.portal.get()
    if 'ca' in portal:
        add_container(
            container=portal['ca'],
            type='Folder',
            title=u"Col·leccions",
            allowed_types=('Collection',),
            exclude_from_nav=True)


def add_predefined_data():
    add_representants_upc()
    add_collections_folder()


def setupVarious(context):
    portal = context.getSite()
    catalog = getToolByName(portal, 'portal_catalog')

    add_catalog_indexes(catalog)
    add_predefined_data()
