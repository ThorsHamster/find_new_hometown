
from yml_reader import YmlReader
from data_handler import DataHandler


class Main:
    def __init__(self):
        self._cities_file = "cities.yml"
        self._settings_file = "settings.yml"

        self._cities = YmlReader(self._cities_file).read()
        self._data_handler = DataHandler()
        self._settings = YmlReader(self._settings_file).read()

    def run(self):
        for city in self._cities['cities']:
            city_1 = self._settings['target_city_1']
            city_2 = city
            print(city_1 + " <-> " + city_2)
            print(self._data_handler.get_distance_duration_between_cities(city_1, city_2))

            city_1 = self._settings['target_city_2']
            city_2 = city
            print(city_1 + " <-> " + city_2)
            print(self._data_handler.get_distance_duration_between_cities(city_1, city_2))


if __name__ == "__main__":
    # execute only if run as a script
    main = Main()
    main.run()
