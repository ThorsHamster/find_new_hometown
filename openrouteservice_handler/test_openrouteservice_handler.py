import pytest
from unittest import TestCase
from unittest.mock import patch

from openrouteservice_handler import OpenRouteServiceHandler


class MockCoordinate:
    def __init__(self):
        self.longitude = 0
        self.latitude = 0


class TestOpenRouteServiceHander(TestCase):

    @patch('openrouteservice_handler.openrouteservice_handler.YmlReader.read')
    def setUp(self, mock_ymlreader):
        mock_ymlreader.return_value = {'api_key': 10}
        self.unit_under_test = OpenRouteServiceHandler()

    @patch('openrouteservice_handler.openrouteservice_handler.openrouteservice.Client.distance_matrix')
    def test_get_distance_duration_between_cities_standard_layout(self, mock_distance_matrix):
        mock_distance_matrix.return_value = {'distances': [[0, 3], [0, 0]], 'durations': [[0, 7], [0, 0]]}

        distance, duration = self.unit_under_test.get_distance_duration_between_cities(MockCoordinate(),
                                                                                       MockCoordinate())
        assert distance == 3
        assert duration == 7

    @patch('openrouteservice_handler.openrouteservice_handler.openrouteservice.Client.distance_matrix')
    def test_get_distance_duration_between_cities_switched_layout(self, mock_distance_matrix):
        mock_distance_matrix.return_value = {'distances': [[0, 0], [3, 0]], 'durations': [[0, 0], [7, 0]]}

        distance, duration = self.unit_under_test.get_distance_duration_between_cities(MockCoordinate(),
                                                                                       MockCoordinate())
        assert distance == 3
        assert duration == 7
