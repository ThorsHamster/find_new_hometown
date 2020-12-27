from typing import Tuple
import openrouteservice
from coordinates import Coordinates


class OpenRouteServiceHandler:
    def __init__(self, openrouteservice_api_key):
        self._api_key = openrouteservice_api_key
        self._client = openrouteservice.Client(key=self._api_key)

    def get_distance_duration_between_cities(self, coordinate_1: Coordinates, coordinate_2: Coordinates) \
            -> Tuple[float, float]:
        coordinates = [[coordinate_1.longitude, coordinate_1.latitude],
                       [coordinate_2.longitude, coordinate_2.latitude]]

        distances = self._client.distance_matrix(locations=coordinates,
                                           metrics=['distance', 'duration'],
                                           units='km')

        if distances is None:
            return 0, 0

        distance_in_km = self._get_value_from_distance_matrix(distances, 'distances')
        duration = self._get_value_from_distance_matrix(distances, 'durations')

        return distance_in_km, duration

    @staticmethod
    def _get_value_from_distance_matrix(distances: dict, value_type: str) -> float:
        value = distances[value_type][0][1]

        if value == 0:
            value = distances[value_type][1][0]
        return value

    def get_coordinate_of_city(self, city_name) -> Coordinates:
        geocode = self._client.pelias_search(text=city_name)

        coordinates = Coordinates()
        if geocode:
            if len(geocode['features']) > 0:
                coordinates.longitude = geocode['features'][0]['geometry']['coordinates'][0]
                coordinates.latitude = geocode['features'][0]['geometry']['coordinates'][1]

        return coordinates
