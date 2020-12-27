import pytest
import gc

from data_handler import DataHandler


class MockCoordinate:
    def __init__(self, longitude=0, latitude=0):
        self.longitude = longitude
        self.latitude = latitude


@pytest.fixture
def unit_under_test(mocker):
    return DataHandler('api_key')


def test_close_database(unit_under_test, mocker):
    mock_sql = mocker.patch('data_handler.data_handler.SqlHandler')

    unit_under_test = DataHandler('api_key')
    unit_under_test.close()

    assert any("close" in str(c) for c in mock_sql.mock_calls)


def test_get_values_between_cities_city_was_already_saved(unit_under_test, mocker):
    mocker.patch('data_handler.data_handler.SqlHandler.get_coordinates_from_city', return_value=MockCoordinate(8, 9))
    mocker.patch('data_handler.data_handler.SqlHandler.set_coordinates_from_city')
    mocker.patch('data_handler.data_handler.SqlHandler.set_distance_duration')
    mocker.patch('data_handler.data_handler.SqlHandler.get_value', return_value=7)
    mocker.patch('data_handler.data_handler.OpenRouteServiceHandler.get_coordinate_of_city',
                 return_value=MockCoordinate(3, 7))

    distance = unit_under_test.get_values_between_cities('city_a', 'city_b', 'distance')

    assert distance == 7


def test_get_values_between_cities_city_not_already_saved_before(unit_under_test, mocker):
    mocker.patch('data_handler.data_handler.SqlHandler.get_coordinates_from_city', return_value=MockCoordinate(0, 0))
    mocker.patch('data_handler.data_handler.SqlHandler.set_coordinates_from_city')
    mocker.patch('data_handler.data_handler.SqlHandler.set_distance_duration')
    mocker.patch('data_handler.data_handler.SqlHandler.get_value', return_value=7)
    mocker.patch('data_handler.data_handler.OpenRouteServiceHandler.get_coordinate_of_city',
                 return_value=MockCoordinate(3, 7))

    distance = unit_under_test.get_values_between_cities('city_a', 'city_b', 'distance')

    assert distance == 7


def test_get_values_between_cities_no_data_saved_before_at_all(unit_under_test, mocker):
    mocker.patch('data_handler.data_handler.SqlHandler.get_coordinates_from_city', return_value=MockCoordinate(8, 9))
    mocker.patch('data_handler.data_handler.SqlHandler.set_coordinates_from_city')
    mocker.patch('data_handler.data_handler.SqlHandler.set_distance_duration')
    mocker.patch('data_handler.data_handler.SqlHandler.get_value', side_effect=[None, 10])
    mocker.patch('data_handler.data_handler.OpenRouteServiceHandler.get_coordinate_of_city',
                 return_value=MockCoordinate(3, 7))
    mocker.patch('data_handler.data_handler.OpenRouteServiceHandler.get_distance_duration_between_cities',
                 return_value=(10, 11))

    distance = unit_under_test.get_values_between_cities('city_a', 'city_b', 'distance')

    assert distance == 10
