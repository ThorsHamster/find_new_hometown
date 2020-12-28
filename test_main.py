from main import run_home_town_finder


def test_script_execution(mocker):
    mocker.patch('home_town_finder.home_town_finder.YmlReader.read', side_effect=[{'cities': 'a'},
                                                                                  {'api_key': 10,
                                                                                   'target_city_1': 'city_A',
                                                                                   'target_city_2': 'city_B',
                                                                                   'option': 'duration'}])
    mock_home_town_finder = mocker.patch('main.HomeTownFinder.run')

    run_home_town_finder()

    mock_home_town_finder.assert_called_once()
