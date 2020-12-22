import pytest

from coordinates import Coordinates


@pytest.fixture
def unit_under_test():
    return Coordinates()


class TestCoordinates:
    def test_longitude(self, unit_under_test):
        unit_under_test.longitude = 3
        assert unit_under_test.longitude == 3

    def test_latitude(self, unit_under_test):
        unit_under_test.latitude = 4
        assert unit_under_test.latitude == 4

    def test_both_elements_with_changes(self, unit_under_test):
        unit_under_test.longitude = 3
        unit_under_test.latitude = 4
        assert unit_under_test.longitude == 3
        assert unit_under_test.latitude == 4

        unit_under_test.longitude = 7
        assert unit_under_test.longitude == 7
        assert unit_under_test.latitude == 4

        unit_under_test.latitude = 9
        assert unit_under_test.longitude == 7
        assert unit_under_test.latitude == 9
