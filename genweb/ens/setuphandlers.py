import os
import csv

from zope.component import getUtility
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes


data_folder_name = 'data'
representants_file_name = 'representants.csv'
fields_to_index = [('estat', 'FieldIndex'),
                   ('figura_juridica', 'FieldIndex'),
                   ('is_historic', 'FieldIndex'),
                   ('data', 'DateIndex'),
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


def add_folder(container, title, allowed_types):
    folder_id = getUtility(IIDNormalizer).normalize(title)
    if folder_id not in container:
        folder = api.content.create(
            type='Folder',
            id=folder_id,
            title=title,
            container=container)
        api.content.transition(
            obj=folder,
            transition='publishtointranet')
        behavior = ISelectableConstrainTypes(folder)
        behavior.setConstrainTypesMode(1)
        behavior.setLocallyAllowedTypes(allowed_types)
        behavior.setImmediatelyAddableTypes(allowed_types)
    return container[folder_id]


def add_representant_upc(folder, title, carrec, is_consell_direccio):
    representant_id = getUtility(IIDNormalizer).normalize(title)
    if representant_id not in folder:
        representant = api.content.create(
            type='genweb.ens.representant',
            id=representant_id,
            title=title,
            container=folder,
            carrec=carrec,
            is_consell_direccio=is_consell_direccio)
        api.content.transition(
            obj=representant,
            transition='publishtointranet')
    return folder[representant_id]


def add_representants_upc():
    portal = api.portal.get()
    if 'ca' in portal:
        representants_folder = add_folder(
            portal['ca'], "Representants UPC", ('genweb.ens.representant',))

        representants_file_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            data_folder_name,
            representants_file_name)

        with open(representants_file_path, 'r') as representants_file:
            for row in csv.reader(representants_file,
                                  delimiter=',', quotechar='"'):
                add_representant_upc(
                    representants_folder,
                    title=row[1].decode('utf-8'),
                    carrec=row[0].decode('utf-8'),
                    is_consell_direccio=True)


def add_predefined_data():
    add_representants_upc()


def setupVarious(context):
    portal = context.getSite()
    catalog = getToolByName(portal, 'portal_catalog')

    add_catalog_indexes(catalog)
    add_predefined_data()
