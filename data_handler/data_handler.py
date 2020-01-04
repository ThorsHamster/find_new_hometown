
from sql_handler import SqlHandler
from openrouteservice_handler import OpenRouteServiceHandler


class DataHandler:
    def __init__(self):
        self._database = SqlHandler()
        self._openrouteservice_handler = OpenRouteServiceHandler()

    def get_distance_duration_between_cities(self, city_1, city_2):
        for city in [city_1, city_2]:
            city_coordinates = self._database.get_coordinates_from_city(city)
            if city_coordinates.longitude == 0 and city_coordinates.latitude == 0:
                city_coordinates = self._openrouteservice_handler.get_coordinate_of_city(city)
                self._database.set_coordinates_from_city(city,
                                                         city_coordinates.longitude,
                                                         city_coordinates.latitude)

        distance = self._database.get_distance(city_1, city_2)
        duration = self._database.get_duration(city_1, city_2)

        if not distance:
            coordinates_1 = self._database.get_coordinates_from_city(city_1)
            coordinates_2 = self._database.get_coordinates_from_city(city_2)
            distance, duration = self._openrouteservice_handler.\
                get_distance_duration_between_cities(coordinates_1,
                                                     coordinates_2)
            self._database.set_distance_duration(city_1, city_2, distance, duration)

        return distance, duration
