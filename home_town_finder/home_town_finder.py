
import pandas as pd
import mplleaflet
import matplotlib.pyplot as plt
from yml_reader import YmlReader
from data_handler import DataHandler


class HomeTownFinder:
    def __init__(self):
        self._cities_file = "cities.yml"
        self._settings_file = "settings.yml"

        self._cities = YmlReader(self._cities_file).read()
        self._data_handler = DataHandler()
        self._settings = YmlReader(self._settings_file).read()

        if not self._cities:
            raise ValueError('cities.yml not valid.')
        if not self._settings:
            raise ValueError('settings.yml not valid.')
        if 'api_key' not in self._settings:
            raise ValueError('setting "api_key" not existing.')
        if not self._settings['api_key']:
            raise ValueError('setting "api_key" not valid.')
        if 'target_city_1' not in self._settings:
            raise ValueError('setting "target_city_1" not existing.')
        if not self._settings['target_city_1']:
            raise ValueError('setting "target_city_1" not valid.')
        if 'target_city_2' not in self._settings:
            raise ValueError('setting "target_city_2" not existing.')
        if not self._settings['target_city_2']:
            raise ValueError('setting "target_city_2" not valid.')
        if 'option' not in self._settings:
            raise ValueError('setting "option" not existing.')
        if not self._settings['option']:
            raise ValueError('setting "option" not valid.')
        self._data_handler.check_valid_option(self._settings['option'])

    def _get_series(self):
        target_city_1_dict = {}
        target_city_2_dict = {}

        for city in self._cities['cities']:
            target_city_1 = self._settings['target_city_1']
            value = self._data_handler.get_values_between_cities(target_city_1,
                                                                 city,
                                                                 self._settings['option'])
            target_city_1_dict[city] = value

            target_city_2 = self._settings['target_city_2']
            value = self._data_handler.get_values_between_cities(target_city_2,
                                                                 city,
                                                                 self._settings['option'])
            target_city_2_dict[city] = value

        target_city_1_series = pd.Series(target_city_1_dict)
        target_city_2_series = pd.Series(target_city_2_dict)

        return target_city_1_series, target_city_2_series

    def _plot_target_cities(self):
        for city in ['target_city_1', 'target_city_2']:
            target_city = self._settings[city]
            coordinates = self._data_handler.get_coordinates_from_city(target_city)
            plt.plot(coordinates.longitude,
                     coordinates.latitude,
                     color='blue',
                     marker='o',
                     markersize=10)

    def run(self):
        target_city_1_series, target_city_2_series = self._get_series()

        # get difference of driving distances
        difference_series = target_city_1_series.subtract(target_city_2_series, fill_value=0.01)
        difference_series = difference_series.abs()

        pd.set_option('display.max_rows', len(difference_series))
        print(difference_series.sort_values(ascending=True))

        mean_difference = difference_series.mean()

        plt.figure()
        self._plot_target_cities()
        for city, value in difference_series.items():
            if value <= 0.2 * mean_difference:
                _color = 'green'
            elif 0.2 * mean_difference < value <= 0.4 * mean_difference:
                _color = 'yellow'
            else:
                _color = 'red'

            coordinates = self._data_handler.get_coordinates_from_city(city)
            plt.plot(coordinates.longitude,
                     coordinates.latitude,
                     color=_color,
                     marker='o',
                     markersize=10)

        mplleaflet.show()
