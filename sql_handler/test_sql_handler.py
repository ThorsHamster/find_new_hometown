import pytest
from unittest.mock import ANY
from sqlite3 import Error

from sql_handler import SqlHandler


@pytest.fixture
def unit_under_test(mocker):
    return SqlHandler()


def test_connect_database_does_not_exist(unit_under_test, mocker):
    mocker.patch('os.path.isfile', return_value=False)
    mocker.patch('sql_handler.sql_handler.sqlite3.connect')

    unit_under_test.connect()

    assert unit_under_test.connected is True


def test_create_database_raises_error(unit_under_test, mocker):
    mocker.patch('os.path.isfile', return_value=False)
    mock_sql = mocker.patch('sql_handler.sql_handler.sqlite3.connect')
    mock_sql.side_effect = Error('Test')

    with pytest.raises(Error, match='Test'):
        unit_under_test.connect()

    assert unit_under_test.connected is False


def test_connect_but_already_connected(unit_under_test, mocker):
    mocker.patch('os.path.isfile', return_value=True)
    mocker.patch('sql_handler.sql_handler.sqlite3.connect')

    unit_under_test.connect()
    unit_under_test.connect()

    assert unit_under_test.connected is True


def test_connect_database_does_already_exist(unit_under_test, mocker):
    mocker.patch('os.path.isfile', return_value=True)
    mocker.patch('sql_handler.sql_handler.sqlite3.connect')

    unit_under_test.connect()

    assert unit_under_test.connected is True


def test_close_not_closed(unit_under_test, mocker):
    mocker.patch('sql_handler.sql_handler.sqlite3.connect')

    unit_under_test.connect()
    unit_under_test.close()

    assert unit_under_test.connected is False


def test_close_already_closed(unit_under_test, mocker):
    mocker.patch('sql_handler.sql_handler.sqlite3.connect')

    unit_under_test.connect()
    unit_under_test.close()
    unit_under_test.close()

    assert unit_under_test.connected is False


def test_get_coordinates_from_city(unit_under_test, mocker):
    mock_sql = mocker.patch('sql_handler.sql_handler.sqlite3.connect')
    mock_sql.return_value.cursor.return_value.fetchone.return_value = [10, 11]

    coordinates = unit_under_test.get_coordinates_from_city('test_city')

    assert coordinates.longitude == 10
    assert coordinates.latitude == 11


def test_set_distance_duration_unknown_city(unit_under_test, mocker):
    mock_sql = mocker.patch('sql_handler.sql_handler.sqlite3.connect')
    mock_sql.return_value.cursor.return_value.fetchone.return_value = None

    with pytest.raises(ValueError, match='City not known.'):
        unit_under_test.set_distance_duration('unknown_city', 'test_city2', 0, 0)


def test_set_coordinates_from_city(unit_under_test, mocker):
    mock_sql = mocker.patch('sql_handler.sql_handler.sqlite3')

    unit_under_test.set_coordinates_from_city('test_city', 1, 2)

    assert mock_sql.connect().cursor().execute.assert_called_with(ANY, ('test_city', 1, 2)) is None


def test_set_distance_duration(unit_under_test, mocker):
    mock_sql = mocker.patch('sql_handler.sql_handler.sqlite3.connect')
    mock_sql.return_value.cursor.return_value.fetchone.side_effect = [[10], [11]]

    unit_under_test.set_distance_duration('test_city', 'test_city2', 30, 40)

    assert any("10, 11, 30, 40" in str(c) for c in mock_sql.mock_calls)


def test_get_value_distance(unit_under_test, mocker):
    mock_sql = mocker.patch('sql_handler.sql_handler.sqlite3.connect')
    mock_sql.return_value.cursor.return_value.fetchone.side_effect = [[10], [11], [45]]

    return_value = unit_under_test.get_value('test_city', 'test_city2', 'distance')

    assert return_value == 45


def test_get_value_duration(unit_under_test, mocker):
    mock_sql = mocker.patch('sql_handler.sql_handler.sqlite3.connect')
    mock_sql.return_value.cursor.return_value.fetchone.side_effect = [[10], [11], [54]]

    return_value = unit_under_test.get_value('test_city', 'test_city2', 'duration')

    assert return_value == 54


def test_get_value_unknown_city(unit_under_test, mocker):
    mock_sql = mocker.patch('sql_handler.sql_handler.sqlite3.connect')
    mock_sql.return_value.cursor.return_value.fetchone.side_effect = [[10], [11], None]

    return_value = unit_under_test.get_value('unkown_city', 'test_city2', 'duration')

    assert return_value is None


def test_get_value_option_not_allowed(unit_under_test, mocker):
    mock_sql = mocker.patch('sql_handler.sql_handler.sqlite3.connect')
    mock_sql.return_value.cursor.return_value.fetchone.side_effect = [[10], [11], None]

    with pytest.raises(ValueError, match='Only "distance" and "duration" allowed.'):
        unit_under_test.get_value('test_city1', 'test_city2', 'not_allowed')
