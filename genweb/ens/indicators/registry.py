# -*- coding: utf-8 -*-

"""
Registry containing the indicators that will be updated on the
external Indicator WS.
"""

from genweb.ens.indicators.beans import Indicator, Category
from genweb.ens.indicators.calculators import (
    EnsNumber, EnsNumberEstat, EnsNumberDelta)


indicators = []
indicators_initialized = False


def initialize(context):
    global indicators_initialized
    if not indicators_initialized:
        register(context)
        indicators_initialized = True


def get_indicators(context):
    initialize(context)
    return indicators


def register(context):
    ens_number = Indicator(
        service='entitats',
        id='ens-n',
        description="Nombre d'ens")
    ens_number.add_category(
        Category(
            id='gabinet-juridic-i-entitats',
            description="Gabinet Jurídic i Entitats",
            calculator=EnsNumber(context, 'gabinet-juridic-i-entitats')))
    ens_number.add_category(
        Category(
            id="gabinet-del-rector",
            description="Gabinet del Rector",
            calculator=EnsNumber(context, 'gabinet-del-rector')))
    indicators.append(ens_number)

    ens_number_actiu = Indicator(
        service="entitats",
        id="ens-n-estat_actiu",
        description="Nombre d'ens en estat actiu")
    ens_number_actiu.add_category(
        Category(
            id="gabinet-juridic-i-entitats",
            description="Gabinet Jurídic i Entitats",
            calculator=EnsNumberEstat(
                context, 'gabinet-juridic-i-entitats', 'Actiu')))
    ens_number_actiu.add_category(
        Category(
            id="gabinet-del-rector",
            description="Gabinet del Rector",
            calculator=EnsNumberEstat(
                context, 'gabinet-del-rector', 'Actiu')))
    indicators.append(ens_number_actiu)

    ens_number_baixa = Indicator(
        service="entitats",
        id="ens-n-estat_baixa",
        description="Nombre d'ens en estat baixa")
    ens_number_baixa.add_category(
        Category(
            id="gabinet-juridic-i-entitats",
            description="Gabinet Jurídic i Entitats",
            calculator=EnsNumberEstat(
                context, 'gabinet-juridic-i-entitats', 'Baixa')))
    ens_number_baixa.add_category(
        Category(
            id="gabinet-del-rector",
            description="Gabinet del Rector",
            calculator=EnsNumberEstat(
                context, 'gabinet-del-rector', 'Baixa')))
    indicators.append(ens_number_baixa)

    ens_number_mes = Indicator(
        service="entitats",
        id="ens-n-data_mes",
        description="Nombre d'ens registrats al darrer mes")
    ens_number_mes.add_category(
        Category(
            id="gabinet-juridic-i-entitats",
            description="Gabinet Jurídic i Entitats",
            calculator=EnsNumberDelta(
                context, 'gabinet-juridic-i-entitats', -30)))
    ens_number_mes.add_category(
        Category(
            id="gabinet-del-rector",
            description="Gabinet del Rector",
            calculator=EnsNumberDelta(
                context, 'gabinet-del-rector', -30)))
    indicators.append(ens_number_mes)

