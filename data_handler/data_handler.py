
from sql_handler import SqlHandler
from openrouteservice_handler import OpenRouteServiceHandler
from coordinates import Coordinates


class DataHandler:
    def __init__(self, openrouteservice_api_key):
        self._database = SqlHandler()
        self._openrouteservice_handler = OpenRouteServiceHandler(openrouteservice_api_key)

    def get_values_between_cities(self, city_1: str, city_2: str, option: str) -> float:

        for city in [city_1, city_2]:
            self.get_coordinates_from_city(city)  # insert into database if not already existing

        if not self._database.get_value(city_1, city_2, option):
            self._load_and_save_distance_and_duration(city_1, city_2)

        return self._database.get_value(city_1, city_2, option)

    def _load_and_save_distance_and_duration(self, city_1: str, city_2: str) -> None:
        coordinates_1 = self._database.get_coordinates_from_city(city_1)
        coordinates_2 = self._database.get_coordinates_from_city(city_2)
        distance, duration = self._openrouteservice_handler. \
            get_distance_duration_between_cities(coordinates_1,
                                                 coordinates_2)
        self._database.set_distance_duration(city_1, city_2, distance, duration)

    def get_coordinates_from_city(self, city: str) -> Coordinates:
        coordinates = self._database.get_coordinates_from_city(city)
        if not self._check_if_coordinates_are_valid(coordinates):
            coordinates = self._load_and_save_new_coordinates(city)

        return coordinates

    def _load_and_save_new_coordinates(self, city: str) -> Coordinates:
        coordinates = self._openrouteservice_handler.get_coordinate_of_city(city)
        self._database.set_coordinates_from_city(city,
                                                 coordinates.longitude,
                                                 coordinates.latitude)
        return coordinates

    @staticmethod
    def _check_if_coordinates_are_valid(coordinates: Coordinates) -> bool:
        return not (coordinates.longitude == 0 and coordinates.latitude == 0)
