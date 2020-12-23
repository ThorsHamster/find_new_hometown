import pytest
from unittest.mock import call

from sql_handler import SqlHandler


class MockCoordinate:
    def __init__(self):
        self.longitude = 0
        self.latitude = 0


@pytest.fixture
def unit_under_test(mocker):
    return SqlHandler()


def test_connect_database_does_not_exist(unit_under_test, mocker):
    mocker.patch('os.path.isfile', return_value=False)
    mocker.patch('sql_handler.sql_handler.sqlite3.connect')

    unit_under_test.connect()

    assert unit_under_test.connected is True


def test_connect_database_does_already_exist(unit_under_test, mocker):
    mocker.patch('os.path.isfile', return_value=True)
    mocker.patch('sql_handler.sql_handler.sqlite3.connect')

    unit_under_test.connect()

    assert unit_under_test.connected is True


def test_close(unit_under_test, mocker):
    mocker.patch('sql_handler.sql_handler.sqlite3.connect')

    unit_under_test.connect()
    unit_under_test.close()

    assert unit_under_test.connected is False


def test_get_coordinates_from_city(unit_under_test, mocker):
    mock_sql = mocker.patch('sql_handler.sql_handler.sqlite3.connect')
    mock_sql.return_value.cursor.return_value.fetchone.return_value = [10, 11]

    coordinates = unit_under_test.get_coordinates_from_city('test_city')

    assert coordinates.longitude == 10
    assert coordinates.latitude == 11


def test_set_coordinates_from_city(unit_under_test, mocker):
    mock_sql = mocker.patch('sql_handler.sql_handler.sqlite3.connect')

    unit_under_test.set_coordinates_from_city('test_city', 0, 0)

    found = False
    for call_ in mock_sql.mock_calls:
        if str(call_) == "call().cursor().execute('INSERT INTO cities (city, longitude, latitude) VALUES (?, ?, ?)', " \
                         "('test_city', 0, 0))":
            found = True
    assert found is True
