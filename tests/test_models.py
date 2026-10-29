import unittest
from datetime import datetime
from unittest.mock import patch

import main_db
import models
import db


class TestModel(unittest.TestCase):

    def test_create_default_location(self):
        main_db.create_default_location()
        main_db.create_default_location()

        location = db.session.get(models.Location, 1)
        self.assertIsNotNone(location)
        self.assertEqual(location.desc_location, 'Cercedilla')
        self.assertEqual(db.session.query(models.Location).count(), 1)

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

    @patch('models.db.session.commit')
    @patch('models.db.session.add')
    def test_write_weather_maps_values_and_persists(self, add, commit):
        weather_data = {
            'metric': {
                'tempHigh': '20.2',
                'tempLow': '9.7',
                'precipTotal': '3.51',
                'windgustHigh': '9.3',
                'pressureMax': '1020.12',
                'pressureMin': '1017.44',
            },
            'humidityHigh': '99',
            'humidityLow': '66',
            'uvHigh': '5',
        }

        models.Weather.write_weather(weather_data)

        saved_weather = add.call_args.args[0]
        self.assertEqual(saved_weather.id_location, 1)
        self.assertIsInstance(saved_weather.date, datetime)
        self.assertEqual(saved_weather.date.tzinfo.zone, 'Europe/Madrid')
        self.assertEqual(saved_weather.temp_high, 20.2)
        self.assertEqual(saved_weather.temp_low, 9.7)
        self.assertEqual(saved_weather.rain_total, 3.51)
        self.assertEqual(saved_weather.humidity_high, 99)
        self.assertEqual(saved_weather.humidity_low, 66)
        self.assertEqual(saved_weather.wind_max, 9.3)
        self.assertEqual(saved_weather.uv_high, 5)
        self.assertEqual(saved_weather.pressure_max, 1020.12)
        self.assertEqual(saved_weather.pressure_min, 1017.44)
        commit.assert_called_once_with()

    def test_no_location(self):
        main_db.create_default_location()
        default_location = db.session.get(models.Location, 1)
        db.session.delete(default_location)
        db.session.commit()
        main_db.create_default_location()

        location = db.session.get(models.Location, 1)
        self.assertIsNotNone(location)
        self.assertEqual(location.desc_location, 'Cercedilla')
        self.assertEqual(db.session.query(models.Location).count(), 1)
