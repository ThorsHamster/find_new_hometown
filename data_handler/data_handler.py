
from sql_handler import SqlHandler
from openrouteservice_handler import OpenRouteServiceHandler


class DataHandler:
    def __init__(self):
        self._database = SqlHandler()
        self._openrouteservice_handler = OpenRouteServiceHandler()

    @staticmethod
    def check_valid_option(option):
        if option not in ['distance', 'duration']:
            raise ValueError('"option" not valid. Use "distance" or "duration".')

    def get_values_between_cities(self, city_1, city_2, option):
        self.check_valid_option(option)

        for city in [city_1, city_2]:
            self.get_coordinates_from_city(city)  # insert into database if not already existing

        value = self._database.get_value(city_1, city_2, option)

        if not value:
            coordinates_1 = self._database.get_coordinates_from_city(city_1)
            coordinates_2 = self._database.get_coordinates_from_city(city_2)
            distance, duration = self._openrouteservice_handler.\
                get_distance_duration_between_cities(coordinates_1,
                                                     coordinates_2)
            self._database.set_distance_duration(city_1, city_2, distance, duration)

        return value

    def get_coordinates_from_city(self, city):
        city_coordinates = self._database.get_coordinates_from_city(city)
        if city_coordinates.longitude == 0 and city_coordinates.latitude == 0:
            city_coordinates = self._openrouteservice_handler.get_coordinate_of_city(city)
            self._database.set_coordinates_from_city(city,
                                                     city_coordinates.longitude,
                                                     city_coordinates.latitude)

        return city_coordinates
