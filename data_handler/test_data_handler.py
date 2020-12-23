import pytest

from data_handler import DataHandler


@pytest.fixture
def unit_under_test(mocker):
    mocker.patch('data_handler.data_handler.OpenRouteServiceHandler')
    mocker.patch('data_handler.data_handler.SqlHandler')
    return DataHandler()


def test_check_valid_option_input_distance(unit_under_test, mocker):
    unit_under_test.check_valid_option('distance')
    assert True


def test_check_valid_option_input_duration(unit_under_test, mocker):
    unit_under_test.check_valid_option('duration')
    assert True


def test_check_valid_option_input_wrong(unit_under_test, mocker):
    with pytest.raises(ValueError, match='"option" not valid. Use "distance" or "duration".'):
        unit_under_test.check_valid_option('something_wrong')
