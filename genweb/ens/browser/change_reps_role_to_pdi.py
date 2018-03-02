# -*- coding: utf-8 -*-

from five import grok
from plone import api
from Products.CMFPlone.interfaces import IPloneSiteRoot


class changeRepsRoleToPDI(grok.View):
    """ Si el col·lectiu d'un representat comença per 'pro' o estrictament
        s'assembla a PDI, es canvia per PDI """
    grok.context(IPloneSiteRoot)
    grok.name('change_reps_role_to_pdi')
    grok.require('cmf.ManagePortal')

    def get_tuple(self, obj):
        return [str(obj.title), str(obj.dni), str(obj.carrec)]

    def valid_obj(self, obj):
        return (str(obj.carrec).lower().startswith('pro') or
                (str(obj.carrec).lower().startswith('pdi') and
                 str(obj.carrec) != 'PDI'))

    def render(self):
        ret = [["[NOM]", "[DNI]", "[PDI]"]]

        list_all = 'list' in self.request.form
        ready = 'ready' in self.request.form
        portal_catalog = api.portal.get_tool(name='portal_catalog')

        if list_all:
            ret[0].append("[CANVI]")

        for rep in portal_catalog(portal_type='genweb.ens.representant',
                                  path='/ens/ca/representants-upc'):
            obj = rep.getObject()
            valid_obj = self.valid_obj(obj)

            if valid_obj or list_all:
                tmp = self.get_tuple(obj)
                if valid_obj and list_all:
                    tmp.append("X")
                ret.append(tmp)

            if valid_obj and ready:
                obj.carrec = 'PDI'
                obj.reindexObject()

        table = '<table>'
        for entry in ret:
            table += '<tr>'
            for info in entry:
                table += '<th style="padding: 2px 10px ' \
                         '2px 10px">%s</th>' % info
            table += '</tr>'
        table += '</table>'

        retstr = []
        if not ready:
            retstr.append("Afegeix <strong>?ready</strong> al URL per "
                          "aplicar els canvis")
        if not list_all:
            retstr.append("Afegeix <strong>?list</strong> al URL per "
                          "mostrar tots els representats i els canvis"
                          " que es faran")
        retstr.append(table)
        return "<br/><br/>".join(retstr)
