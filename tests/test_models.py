import unittest

import main_db
import models
import db


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
        weather.id_location = 1
        weather.temp_high = 20
        self.assertEqual(repr(weather), 'Weather(1, 20)')

    def test_no_location(self):
        default_location = db.session.get(models.Location, 1)
        db.session.delete(default_location)
        db.session.commit()
        main_db.create_default_location()
