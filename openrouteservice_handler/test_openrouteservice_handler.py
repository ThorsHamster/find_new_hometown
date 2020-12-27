import pytest

from openrouteservice_handler import OpenRouteServiceHandler


class MockCoordinate:
    def __init__(self):
        self.longitude = 0
        self.latitude = 0


@pytest.fixture
def unit_under_test(mocker):
    return OpenRouteServiceHandler('api_key')


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


def test_get_coordinate_of_city_city_found(unit_under_test, mocker):
    mocker.patch('openrouteservice_handler.openrouteservice_handler.openrouteservice.Client.pelias_search',
                 return_value={'features': [{'geometry': {'coordinates': [3, 7]}}]})

    coordinates = unit_under_test.get_coordinate_of_city('test_city')

    assert coordinates.longitude == 3
    assert coordinates.latitude == 7


def test_get_coordinate_of_city_city_not_found(unit_under_test, mocker):
    mocker.patch('openrouteservice_handler.openrouteservice_handler.openrouteservice.Client.pelias_search',
                 return_value=None)

    coordinates = unit_under_test.get_coordinate_of_city('test_city')

    assert coordinates.longitude == 0
    assert coordinates.latitude == 0
