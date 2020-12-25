import pytest

from main import run_home_town_finder


def test_script_execution(mocker):
    mock_home_town_finder = mocker.patch('main.HomeTownFinder.run')

    run_home_town_finder()

    assert mock_home_town_finder.called
