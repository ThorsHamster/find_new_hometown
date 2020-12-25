import pytest

from home_town_finder import HomeTownFinder


def test_home_town_finder_initialize_data(mocker):
    mocker.patch('home_town_finder.home_town_finder.YmlReader.read', side_effect=[{'cities': 'a'},
                                                                          {'api_key': 10,
                                                                           'target_city_1': 'city_A',
                                                                           'target_city_2': 'city_B',
                                                                           'option': 'duration'}])
    mock_data_handler = mocker.patch('home_town_finder.home_town_finder.DataHandler')
    mock_data_handler.return_value.check_valid_option.return_value = True

    HomeTownFinder()


def test_home_town_finder_initialize_data_invalid_cities_yml(mocker):
    mocker.patch('home_town_finder.home_town_finder.YmlReader.read', side_effect=[None,
                                                                          {'api_key': 10,
                                                                           'target_city_1': 'city_A',
                                                                           'target_city_2': 'city_B',
                                                                           'option': 'duration'}])
    mock_data_handler = mocker.patch('home_town_finder.home_town_finder.DataHandler')
    mock_data_handler.return_value.check_valid_option.return_value = True

    with pytest.raises(ValueError, match='cities.yml not valid.'):
        HomeTownFinder()


def test_home_town_finder_initialize_data_invalid_api_key(mocker):
    mocker.patch('home_town_finder.home_town_finder.YmlReader.read', side_effect=[{'cities': 'a'},
                                                                          {'api_key': None,
                                                                           'target_city_1': 'city_A',
                                                                           'target_city_2': 'city_B',
                                                                           'option': 'duration'}])
    mock_data_handler = mocker.patch('home_town_finder.home_town_finder.DataHandler')
    mock_data_handler.return_value.check_valid_option.return_value = True

    with pytest.raises(ValueError, match='setting "api_key" not valid.'):
        HomeTownFinder()


def test_home_town_finder_initialize_data_invalid_target_city_1(mocker):
    mocker.patch('home_town_finder.home_town_finder.YmlReader.read', side_effect=[{'cities': 'a'},
                                                                          {'api_key': 10,
                                                                           'target_city_1': None,
                                                                           'target_city_2': 'city_B',
                                                                           'option': 'duration'}])
    mock_data_handler = mocker.patch('home_town_finder.home_town_finder.DataHandler')
    mock_data_handler.return_value.check_valid_option.return_value = True

    with pytest.raises(ValueError, match='setting "target_city_1" not valid.'):
        HomeTownFinder()


def test_home_town_finder_initialize_data_invalid_target_city_2(mocker):
    mocker.patch('home_town_finder.home_town_finder.YmlReader.read', side_effect=[{'cities': 'a'},
                                                                          {'api_key': 10,
                                                                           'target_city_1': 'city_A',
                                                                           'target_city_2': None,
                                                                           'option': 'duration'}])
    mock_data_handler = mocker.patch('home_town_finder.home_town_finder.DataHandler')
    mock_data_handler.return_value.check_valid_option.return_value = True

    with pytest.raises(ValueError, match='setting "target_city_2" not valid.'):
        HomeTownFinder()


def test_home_town_finder_initialize_data_invalid_option(mocker):
    mocker.patch('home_town_finder.home_town_finder.YmlReader.read', side_effect=[{'cities': 'a'},
                                                                          {'api_key': 10,
                                                                           'target_city_1': 'city_A',
                                                                           'target_city_2': 'city_B',
                                                                           'option': None}])
    mock_data_handler = mocker.patch('home_town_finder.home_town_finder.DataHandler')
    mock_data_handler.return_value.check_valid_option.return_value = True

    with pytest.raises(ValueError, match='setting "option" not valid.'):
        HomeTownFinder()
