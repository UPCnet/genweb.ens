# -*- coding: utf-8 -*-
"""Unit tests for data access functions."""

import unittest
from mock import Mock, patch

from genweb.ens.data_access.ens import EnsDataReporter


class MockCatalog(object):
    def searchResults(self, *args, **kwargs):
        return []


class TestDataAccess(unittest.TestCase):
    """Test data access functions."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.catalog = MockCatalog()

    def test_list_carrecs_by_organ_grouped_by_ens_obj(self):
        reporter = EnsDataReporter(self.catalog)

        # No carrecs related to the organ
        with patch(
                'genweb.ens.tests.test_data_access.MockCatalog.searchResults',
                Mock(side_effect=([], []))):
            carrecs = reporter.list_carrecs_by_organ_grouped_by_ens_obj(Mock())

            self.assertEqual(carrecs, [])

        # Only UPC carrecs related to the organ
        upc_carrecs = [Mock(getObject=lambda: 1),
                       Mock(getObject=lambda: 2)]
        with patch(
                'genweb.ens.tests.test_data_access.MockCatalog.searchResults',
                Mock(side_effect=(upc_carrecs, []))):
            carrecs = reporter.list_carrecs_by_organ_grouped_by_ens_obj(Mock())

            self.assertEqual(len(carrecs), 1)

            self.assertEqual(carrecs[0][0], 'UPC')
            self.assertEqual(carrecs[0][1], [1, 2])

        # Only non-UPC carrecs related to the organ
        not_upc_carrecs = [Mock(getObject=lambda: Mock(ens='B', title='B1')),
                           Mock(getObject=lambda: Mock(ens='A', title='A1')),
                           Mock(getObject=lambda: Mock(ens='B', title='B2')),
                           Mock(getObject=lambda: Mock(ens='C', title='C1')),
                           Mock(getObject=lambda: Mock(ens='B', title='B3')),
                           Mock(getObject=lambda: Mock(ens='A', title='A2'))]
        with patch(
                'genweb.ens.tests.test_data_access.MockCatalog.searchResults',
                Mock(side_effect=([], not_upc_carrecs))):
            carrecs = reporter.list_carrecs_by_organ_grouped_by_ens_obj(Mock())

            self.assertEqual([carrec[0] for carrec in carrecs],
                             ['A', 'B', 'C'])

            self.assertEqual([c.title for c in carrecs[0][1]], ['A1', 'A2'])
            self.assertEqual([c.title for c in carrecs[1][1]],
                             ['B1', 'B2', 'B3'])
            self.assertEqual([c.title for c in carrecs[2][1]], ['C1'])

        # Both UPC and non-UPC carrecs related to the organ
        with patch(
                'genweb.ens.tests.test_data_access.MockCatalog.searchResults',
                Mock(side_effect=(upc_carrecs, not_upc_carrecs))):
            carrecs = reporter.list_carrecs_by_organ_grouped_by_ens_obj(Mock())

            self.assertEqual([carrec[0] for carrec in carrecs],
                             ['UPC', 'A', 'B', 'C'])

            self.assertEqual(carrecs[0][1], [1, 2])
            self.assertEqual([c.title for c in carrecs[1][1]], ['A1', 'A2'])
            self.assertEqual([c.title for c in carrecs[2][1]],
                             ['B1', 'B2', 'B3'])
            self.assertEqual([c.title for c in carrecs[3][1]], ['C1'])
