from main import run_home_town_finder


def test_script_execution(mocker):
    mock_home_town_finder = mocker.patch('main.HomeTownFinder')

    run_home_town_finder()

    assert any("run" in str(c) for c in mock_home_town_finder.mock_calls)
