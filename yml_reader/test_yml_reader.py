import pytest
from unittest.mock import mock_open

from yml_reader import YmlReader


@pytest.fixture
def unit_under_test(mocker):
    return YmlReader("test_file")


def test_read_file_exists(unit_under_test, mocker):
    mocker.patch('os.path.isfile', return_value=True)
    mocker.patch('builtins.open', mock_open())
    mocker.patch('yaml.safe_load', return_value="yaml_content")

    yaml_content = unit_under_test.read()

    assert yaml_content == "yaml_content"


def test_read_file_does_not_exists(unit_under_test, mocker):
    mocker.patch('os.path.isfile', return_value=False)
    mocker.patch('sys.exit')

    yaml_content = unit_under_test.read()

    assert yaml_content is None
