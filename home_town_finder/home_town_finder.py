from typing import Tuple
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

        self._difference_series = None

    def _check_preconditions(self) -> None:
        self._check_preconditions_cities()
        self._check_preconditions_settings()

    def _check_preconditions_cities(self) -> None:
        if not self._cities:
            raise ValueError(f'{self._cities_file} not valid.')
        if self._cities[self._cities_field] is None:
            raise ValueError(f'{self._cities_field} are empty.')

    def _check_preconditions_settings(self) -> None:
        if not self._settings:
            raise ValueError(f'{self._settings_file} not valid.')
        self._check_preconditions_settings_api_key()
        self._check_preconditions_settings_target_city_1()
        self._check_preconditions_settings_target_city_2()
        self._check_preconditions_settings_option()

    def _check_preconditions_settings_api_key(self) -> None:
        if self._api_key not in self._settings:
            raise ValueError(f'setting "{self._api_key}" not existing.')
        if not self._settings[self._api_key]:
            raise ValueError(f'setting "{self._api_key}" not valid.')

    def _check_preconditions_settings_target_city_1(self) -> None:
        if self._target_city_1 not in self._settings:
            raise ValueError(f'setting "{self._target_city_1}" not existing.')
        if not self._settings[self._target_city_1]:
            raise ValueError(f'setting "{self._target_city_1}" not valid.')

    def _check_preconditions_settings_target_city_2(self) -> None:
        if self._target_city_2 not in self._settings:
            raise ValueError(f'setting "{self._target_city_2}" not existing.')
        if not self._settings[self._target_city_2]:
            raise ValueError(f'setting "{self._target_city_2}" not valid.')

    def _check_preconditions_settings_option(self) -> None:
        if self._option not in self._settings:
            raise ValueError(f'setting "{self._option}" not existing.')
        if not self._settings[self._option]:
            raise ValueError(f'setting "{self._option}" not valid.')
        if not self._settings[self._option] in ['distance', 'duration']:
            raise ValueError(f'value of setting "{self._option}" not valid. Use "duration" or "distance".')

    def _get_series(self) -> Tuple[pd.Series, pd.Series]:
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

    def _get_values_between_city_and_target_city(self, city: str, target_city: str) -> float:
        return self._data_handler.get_values_between_cities(target_city,
                                                            city,
                                                            self._settings[self._option])

    @staticmethod
    def _convert_dict_into_pandas_series(dictionary: dict) -> pd.Series:
        return pd.Series(dictionary)

    def _plot_target_cities(self) -> None:
        for target_city in [self._target_city_1, self._target_city_2]:
            self._plot_single_city(self._settings[target_city], color_='blue')

    def _plot_cities(self) -> None:
        for city, value in self._difference_series.items():
            self._plot_single_city(city, color_=self._get_color_code_of_city(value))

    def _plot_single_city(self, city: str, color_: str) -> None:
        coordinates = self._data_handler.get_coordinates_from_city(city)
        plt.plot(coordinates.longitude,
                 coordinates.latitude,
                 color=color_,
                 marker='o',
                 markersize=10)

    def _get_color_code_of_city(self, value: float) -> str:
        mean_difference = self._difference_series.mean()
        if value <= 0.2 * mean_difference:
            _color = 'green'
        elif 0.2 * mean_difference < value <= 0.4 * mean_difference:
            _color = 'yellow'
        else:
            _color = 'red'
        return _color

    def _print_cities_on_console(self) -> None:
        pd.set_option('display.max_rows', len(self._difference_series))
        print(self._difference_series.sort_values(ascending=True))

    def _get_difference_series(self) -> pd.Series:
        target_city_1_series, target_city_2_series = self._get_series()

        # get difference of driving distances
        difference_series = target_city_1_series.subtract(target_city_2_series, fill_value=0.01)
        return difference_series.abs()

    def run(self) -> None:
        self._difference_series = self._get_difference_series()

        self._print_cities_on_console()

        plt.figure()
        self._plot_target_cities()
        self._plot_cities()

        mplleaflet.show()
