import pandas as pd
import mplleaflet
import matplotlib.pyplot as plt
from yml_reader import YmlReader
from data_handler import DataHandler


class HomeTownFinder:
    def __init__(self):
        self._cities_file = "cities.yml"
        self._settings_file = "settings.yml"

        self._cities_field = 'cities'
        self._target_city_1 = 'target_city_1'
        self._target_city_2 = 'target_city_2'
        self._option = 'option'
        self._api_key = 'api_key'

        self._cities = YmlReader(self._cities_file).read()
        self._data_handler = DataHandler()
        self._settings = YmlReader(self._settings_file).read()

        self._check_preconditions()

    def _check_preconditions(self):
        if not self._cities:
            raise ValueError(f'{self._cities_file} not valid.')
        if self._cities[self._cities_field] is None:
            raise ValueError(f'{self._cities_field} are empty.')
        if not self._settings:
            raise ValueError(f'{self._settings_file} not valid.')
        if self._api_key not in self._settings:
            raise ValueError(f'setting "{self._api_key}" not existing.')
        if not self._settings[self._api_key]:
            raise ValueError(f'setting "{self._api_key}" not valid.')
        if self._target_city_1 not in self._settings:
            raise ValueError(f'setting "{self._target_city_1}" not existing.')
        if not self._settings[self._target_city_1]:
            raise ValueError(f'setting "{self._target_city_1}" not valid.')
        if self._target_city_2 not in self._settings:
            raise ValueError(f'setting "{self._target_city_2}" not existing.')
        if not self._settings[self._target_city_2]:
            raise ValueError(f'setting "{self._target_city_2}" not valid.')
        if self._option not in self._settings:
            raise ValueError(f'setting "{self._option}" not existing.')
        if not self._settings[self._option]:
            raise ValueError(f'setting "{self._option}" not valid.')
        if not self._settings[self._option] in ['distance', 'duration']:
            raise ValueError(f'value of setting "{self._option}" not valid. Use "duration" or "distance".')

    def _get_series(self):
        target_city_1_dict = {}
        target_city_2_dict = {}

        for city in self._cities[self._cities_field]:
            target_city_1_dict[city] = self._get_values_between_city_and_target_city(city,
                                                                                     self._settings[
                                                                                         self._target_city_1])

            target_city_2_dict[city] = self._get_values_between_city_and_target_city(city,
                                                                                     self._settings[
                                                                                         self._target_city_2])

        return self._convert_dict_into_pandas_series(target_city_1_dict), self._convert_dict_into_pandas_series(
            target_city_2_dict)

    def _get_values_between_city_and_target_city(self, city, target_city):
        return self._data_handler.get_values_between_cities(target_city,
                                                            city,
                                                            self._settings[self._option])

    @staticmethod
    def _convert_dict_into_pandas_series(dictionary):
        return pd.Series(dictionary)

    def _plot_target_cities(self):
        for city in [self._target_city_1, self._target_city_2]:
            target_city = self._settings[city]
            coordinates = self._data_handler.get_coordinates_from_city(target_city)
            plt.plot(coordinates.longitude,
                     coordinates.latitude,
                     color='blue',
                     marker='o',
                     markersize=10)

    def _plot_cities(self, difference_series, mean_difference):
        for city, value in difference_series.items():
            coordinates = self._data_handler.get_coordinates_from_city(city)
            plt.plot(coordinates.longitude,
                     coordinates.latitude,
                     color=self._get_color_code_of_city(value, mean_difference),
                     marker='o',
                     markersize=10)

    @staticmethod
    def _get_color_code_of_city(value, mean_difference):
        if value <= 0.2 * mean_difference:
            _color = 'green'
        elif 0.2 * mean_difference < value <= 0.4 * mean_difference:
            _color = 'yellow'
        else:
            _color = 'red'
        return _color

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
        self._plot_cities(difference_series, mean_difference)

        mplleaflet.show()
