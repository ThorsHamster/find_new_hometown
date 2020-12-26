import pytest

from home_town_finder import HomeTownFinder


class MockPandasSeries:

    def __init__(self, _items_return_value):
        self._items_return_value = _items_return_value

    def __len__(self):
        return 1

    def subtract(self, serie, fill_value):
        return self

    def abs(self):
        return self

    def mean(self):
        return 1

    def sort_values(self, ascending):
        pass

    def items(self):
        return self._items_return_value


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


def test_home_town_finder_initialize_data_invalid_settings_yml(mocker):
    mocker.patch('home_town_finder.home_town_finder.YmlReader.read', side_effect=[{'cities': 'a'},
                                                                                  None])
    mock_data_handler = mocker.patch('home_town_finder.home_town_finder.DataHandler')
    mock_data_handler.return_value.check_valid_option.return_value = True

    with pytest.raises(ValueError, match='settings.yml not valid.'):
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


def test_home_town_finder_run(mocker):
    mocker.patch('home_town_finder.home_town_finder.YmlReader.read', side_effect=[{'cities': 'a'},
                                                                                  {'api_key': 10,
                                                                                   'target_city_1': 'city_A',
                                                                                   'target_city_2': 'city_B',
                                                                                   'option': 'distance'}])
    mock_data_handler = mocker.patch('home_town_finder.home_town_finder.DataHandler')
    mock_data_handler.return_value.check_valid_option.return_value = True
    mock_plt = mocker.patch('home_town_finder.home_town_finder.plt')
    mock_mplleaflet = mocker.patch('home_town_finder.home_town_finder.mplleaflet')
    mock_pandas = mocker.patch('home_town_finder.home_town_finder.pd.Series')
    mock_pandas.return_value = MockPandasSeries([['test_city', 0.1], ['test_city', 0.35], ['test_city', 0.9]])

    unit_under_test = HomeTownFinder()
    unit_under_test.run()

    assert mock_mplleaflet.show.called
    assert mock_plt.plot.called
