import pytest

from openrouteservice_handler import OpenRouteServiceHandler


class MockCoordinate:
    def __init__(self):
        self.longitude = 0
        self.latitude = 0


@pytest.fixture
def unit_under_test(mocker):
    mocker.patch('openrouteservice_handler.openrouteservice_handler.YmlReader.read', return_value={'api_key': 10})
    return OpenRouteServiceHandler()


def test_get_distance_duration_between_cities_standard_layout(unit_under_test, mocker):
    mocker.patch('openrouteservice_handler.openrouteservice_handler.openrouteservice.Client.distance_matrix',
                 return_value={'distances': [[0, 3], [0, 0]], 'durations': [[0, 7], [0, 0]]})

    distance, duration = unit_under_test.get_distance_duration_between_cities(MockCoordinate(),
                                                                              MockCoordinate())
    assert distance == 3
    assert duration == 7


def test_get_distance_duration_between_cities_switched_layout(unit_under_test, mocker):
    mocker.patch('openrouteservice_handler.openrouteservice_handler.openrouteservice.Client.distance_matrix',
                 return_value={'distances': [[0, 0], [3, 0]], 'durations': [[0, 0], [7, 0]]})

    distance, duration = unit_under_test.get_distance_duration_between_cities(MockCoordinate(),
                                                                              MockCoordinate())
    assert distance == 3
    assert duration == 7


def test_get_distance_duration_between_cities_no_return_value(unit_under_test, mocker):
    mocker.patch('openrouteservice_handler.openrouteservice_handler.openrouteservice.Client.distance_matrix',
                 return_value=None)

    distance, duration = unit_under_test.get_distance_duration_between_cities(MockCoordinate(),
                                                                              MockCoordinate())
    assert distance == 0
    assert duration == 0
