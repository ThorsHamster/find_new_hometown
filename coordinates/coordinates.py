
class Coordinates:
    def __init__(self):
        self._longitude = 0
        self._latitude = 0

    @property
    def longitude(self) -> int:
        return self._longitude

    @longitude.setter
    def longitude(self, value: int) -> None:
        self._longitude = value

    @property
    def latitude(self) -> int:
        return self._latitude

    @latitude.setter
    def latitude(self, value: int) -> None:
        self._latitude = value
