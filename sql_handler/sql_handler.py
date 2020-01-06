
import os
import sqlite3
from sqlite3 import Error
from coordinates import Coordinates


class SqlHandler:
    def __init__(self):
        self._database = "data.db"
        self._connection = None
        self._cursor = None
        self.connected = False

    def _create_new(self):
        try:
            if os.path.isfile(self._database):
                print("Database already exists.")
                return

            self._connection = sqlite3.connect(self._database)
            self._cursor = self._connection.cursor()

            sql_table_cities_create = """
                CREATE TABLE cities (
                    id integer PRIMARY KEY,
                    city text NOT NULL,
                    longitude REAL,
                    latitude REAL
                    )
                    """
            self._cursor.execute(sql_table_cities_create)

            sql_table_distances_create = """
                CREATE TABLE distances (
                    city_1_id integer,
                    city_2_id integer,
                    distance REAL,
                    duration REAL
                    )
                    """
            self._cursor.execute(sql_table_distances_create)

            self._connection.commit()
            self._connection.close()

        except Error as error:
            print(error)

    def _get_city_id(self, city):
        if not self.connected:
            self.connect()

        sql_string = "SELECT id FROM cities WHERE city = ?"
        self._cursor.execute(sql_string, (city,))
        answer = self._cursor.fetchone()
        if answer:
            answer = answer[0]
        return answer

    def connect(self):
        try:
            if self.connected:
                return
            if not os.path.isfile(self._database):
                self._create_new()

            self._connection = sqlite3.connect(self._database)
            self._cursor = self._connection.cursor()
            self.connected = True
        except Error as error:
            print(error)

    def close(self):
        self._connection.close()
        self.connected = False

    def get_coordinates_from_city(self, city):
        if not self.connected:
            self.connect()

        sql_string = "SELECT longitude, latitude FROM cities WHERE city = ?"
        self._cursor.execute(sql_string, (city,))

        answer = self._cursor.fetchone()

        coordinates = Coordinates()
        if answer:
            coordinates.longitude = answer[0]
            coordinates.latitude = answer[1]

        return coordinates

    def set_coordinates_from_city(self, city, longitude, latitude):
        if not self.connected:
            self.connect()

        sql_string = "INSERT INTO cities (city, longitude, latitude) VALUES (?, ?, ?)"
        self._cursor.execute(sql_string, (city, longitude, latitude,))
        self._connection.commit()

    def set_distance_duration(self, city_1, city_2, distance, duration):
        if not self.connected:
            self.connect()

        city_1_id = self._get_city_id(city_1)
        city_2_id = self._get_city_id(city_2)

        sql_string = "INSERT INTO distances (city_1_id, city_2_id, distance, duration) " \
                     "VALUES (?, ?, ?, ?)"
        self._cursor.execute(sql_string, (city_1_id, city_2_id, distance, duration,))
        self._connection.commit()

    def get_value(self, city_1, city_2, which_value):
        if not self.connected:
            self.connect()

        city_1_id = self._get_city_id(city_1)
        city_2_id = self._get_city_id(city_2)

        if which_value == 'distance':
            sql_string = "SELECT distance FROM distances WHERE " \
                         "(city_1_id = ? AND city_2_id = ?)" \
                         " OR (city_1_id = ? AND city_2_id = ?)"
        else:
            sql_string = "SELECT duration FROM distances WHERE " \
                         "(city_1_id = ? AND city_2_id = ?)" \
                         " OR (city_1_id = ? AND city_2_id = ?)"
        self._cursor.execute(sql_string, (city_1_id, city_2_id, city_2_id, city_1_id,))
        answer = self._cursor.fetchone()
        if answer:
            answer = answer[0]
        return answer
