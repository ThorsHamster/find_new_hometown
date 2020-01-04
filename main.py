
import pandas as pd
from yml_reader import YmlReader
from data_handler import DataHandler


class Main:
    def __init__(self):
        self._cities_file = "cities.yml"
        self._settings_file = "settings.yml"

        self._cities = YmlReader(self._cities_file).read()
        self._data_handler = DataHandler()
        self._settings = YmlReader(self._settings_file).read()

    def _get_distance_series(self):
        target_city_1_dict = {}
        target_city_2_dict = {}

        for city in self._cities['cities']:
            target_city_1 = self._settings['target_city_1']
            distance, _ = self._data_handler.get_distance_duration_between_cities(target_city_1,
                                                                                  city)
            target_city_1_dict[city] = distance

            target_city_2 = self._settings['target_city_2']
            distance, _ = self._data_handler.get_distance_duration_between_cities(target_city_2,
                                                                                  city)
            target_city_2_dict[city] = distance

        target_city_1_series = pd.Series(target_city_1_dict)
        target_city_2_series = pd.Series(target_city_2_dict)

        return target_city_1_series, target_city_2_series

    def run(self):
        target_city_1_series, target_city_2_series = self._get_distance_series()

        # get difference of driving distances
        difference_series = target_city_1_series.subtract(target_city_2_series, fill_value=0.01)
        difference_series = difference_series.abs()

        pd.set_option('display.max_rows', len(difference_series))
        print(difference_series.sort_values(ascending=True))


if __name__ == "__main__":
    # execute only if run as a script
    MAIN = Main()
    MAIN.run()
