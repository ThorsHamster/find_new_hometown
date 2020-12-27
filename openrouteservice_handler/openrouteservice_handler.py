
from typing import Tuple
import openrouteservice
from yml_reader import YmlReader
from coordinates import Coordinates


class OpenRouteServiceHandler:
    def __init__(self):
        self._settings_file = "settings.yml"
        self._settings = YmlReader(self._settings_file).read()

    def get_distance_duration_between_cities(self, coordinate_1, coordinate_2) -> Tuple[float, float]:
        coordinates = [[coordinate_1.longitude, coordinate_1.latitude],
                       [coordinate_2.longitude, coordinate_2.latitude]]

        client = openrouteservice.Client(key=self._settings['api_key'])
        distances = client.distance_matrix(locations=coordinates,
                                           metrics=['distance', 'duration'],
                                           units='km')

        if distances is None:
            return 0, 0

        distance_in_km = distances['distances'][0][1]
        duration = distances['durations'][0][1]

        if distance_in_km == 0:
            distance_in_km = distances['distances'][1][0]

        if duration == 0:
            duration = distances['durations'][1][0]

        return distance_in_km, duration

    def get_coordinate_of_city(self, city_name) -> Coordinates:
        client = openrouteservice.Client(key=self._settings['api_key'])
        geocode = client.pelias_search(text=city_name)

        coordinates = Coordinates()
        if geocode:
            if len(geocode['features']) > 0:
                coordinates.longitude = geocode['features'][0]['geometry']['coordinates'][0]
                coordinates.latitude = geocode['features'][0]['geometry']['coordinates'][1]

        return coordinates
