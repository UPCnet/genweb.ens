# -*- coding: utf-8 -*-
"""Unit tests for helper functions."""

import unittest
from mock import Mock

from genweb.ens import _
from genweb.ens.content.ens import (get_denominacio,
                                    get_percentatge_participacio,
                                    get_aportacio, get_quota,
                                    get_capital_social, get_seu_social)


class TestHelpers(unittest.TestCase):
    """Test helper functions."""

    def test_ens_get_denominacio(self):
        self.assertEqual(
            u"Amnistía Internacional",
            get_denominacio(Mock(title=u"Amnistía Internacional",
                                 acronim=None)))

        self.assertEqual(
            u"Amnistía Internacional (AÍ)",
            get_denominacio(Mock(title=u"Amnistía Internacional",
                                 acronim=u"AÍ")))

    def test_ens_get_percentatge_participacio(self):
        self.assertEqual(
            "-",
            get_percentatge_participacio(Mock(percentatge_participacio=None)))

        self.assertEqual(
            "2.00%",
            get_percentatge_participacio(Mock(percentatge_participacio=2)))

        self.assertEqual(
            "2.35%",
            get_percentatge_participacio(Mock(percentatge_participacio=2.35)))

    def test_ens_get_aportacio(self):
        self.assertEqual(
            "-",
            get_aportacio(Mock(aportacio_sn=None)))

        self.assertEqual(
            _(u"No"),
            get_aportacio(Mock(aportacio_sn=False)))

        self.assertEqual(
            _(u"Sí"),
            get_aportacio(Mock(aportacio_sn=True, aportacio_import=None)))

        self.assertEqual(
            _(u"2.00"),
            get_aportacio(Mock(aportacio_sn=True,
                               aportacio_import=2,
                               aportacio_moneda=None)))

        self.assertEqual(
            u"2.00 €/any",
            get_aportacio(Mock(aportacio_sn=True,
                               aportacio_import=2,
                               aportacio_moneda=u"€/any")))

        self.assertEqual(
            u"2.35 €/any",
            get_aportacio(Mock(aportacio_sn=True,
                               aportacio_import=2.35,
                               aportacio_moneda=u"€/any")))

    def test_ens_get_quota(self):
        self.assertEqual(
            "-",
            get_quota(Mock(quota_sn=None)))

        self.assertEqual(
            _(u"No"),
            get_quota(Mock(quota_sn=False)))

        self.assertEqual(
            _(u"Sí"),
            get_quota(Mock(quota_sn=True, quota_import=None)))

        self.assertEqual(
            _(u"2.00"),
            get_quota(Mock(quota_sn=True,
                           quota_import=2,
                           quota_moneda=None)))

        self.assertEqual(
            u"2.00 €/any",
            get_quota(Mock(quota_sn=True,
                           quota_import=2,
                           quota_moneda=u"€/any")))

        self.assertEqual(
            u"2.35 €/any",
            get_quota(Mock(quota_sn=True,
                           quota_import=2.35,
                           quota_moneda=u"€/any")))

    def test_ens_get_capital_social(self):
        self.assertEqual(
            "-",
            get_capital_social(Mock(capital_social_sn=None)))

        self.assertEqual(
            _(u"No"),
            get_capital_social(Mock(capital_social_sn=False)))

        self.assertEqual(
            _(u"Sí"),
            get_capital_social(Mock(capital_social_sn=True,
                                    capital_social_import=None)))

        self.assertEqual(
            _(u"2.00"),
            get_capital_social(Mock(capital_social_sn=True,
                                    capital_social_import=2,
                                    capital_social_moneda=None)))

        self.assertEqual(
            u"2.00 €/any",
            get_capital_social(Mock(capital_social_sn=True,
                                    capital_social_import=2,
                                    capital_social_moneda=u"€/any")))

        self.assertEqual(
            u"2.35 €/any",
            get_capital_social(Mock(capital_social_sn=True,
                                    capital_social_import=2.35,
                                    capital_social_moneda=u"€/any")))

    def test_ens_get_seu_social(self):
        self.assertEqual(
            "-",
            get_seu_social(Mock(seu_social=None)))

        self.assertEqual(
            u"Espanya",
            get_seu_social(Mock(seu_social=u"Espanya")))

        self.assertEqual(
            u"Estranger",
            get_seu_social(Mock(seu_social=u"Estranger",
                                seu_social_estranger=None)))

        self.assertEqual(
            u"Connemara",
            get_seu_social(Mock(seu_social=u"Estranger",
                                seu_social_estranger="Connemara")))
