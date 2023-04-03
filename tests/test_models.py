import unittest

from parrao_weather_bot import main_db, models


class TestModel(unittest.TestCase):

    def test_create_default_location(self):
        main_db.create_default_location()

    def test_init_location(self):
        location = models.Location(id_location=1, desc_location='A location')
        self.assertIsNotNone(location)
        print(location)
        self.assertEqual(repr(location), 'Location(1, A location)')

    def test_weather(self):
        weather = models.Weather()
        self.assertIsNotNone(weather)
        print(weather)
