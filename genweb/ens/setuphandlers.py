from Products.CMFCore.utils import getToolByName

fields_to_index = [('estat', 'FieldIndex'),
                   ('figura_juridica', 'FieldIndex'),
                   ('is_directiu', 'FieldIndex'),
                   ('is_contacte', 'FieldIndex'),
                   ('is_vigent', 'FieldIndex'),
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


def setupVarious(context):
    portal = context.getSite()
    catalog = getToolByName(portal, 'portal_catalog')

    add_catalog_indexes(catalog)
