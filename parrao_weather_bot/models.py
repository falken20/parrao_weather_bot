from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
import pytz  # Work with time zones

import db


class Location(db.Base):
    __tablename__ = 't_location'

    id_location = Column(Integer, primary_key=True)
    desc_location = Column(String, nullable=False)

    def __init__(self, id_location, desc_location):
        self.id_location = id_location
        self.desc_location = desc_location

    def __repr__(self) -> str:
        return f"Location({self.id_location}, {self.desc_location})"

    def __str__(self) -> str:
        return self.desc_location


class Weather(db.Base):
    __tablename__ = 't_weather'

    id = Column(Integer, primary_key=True)
    id_location = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    temp_high = Column(Float)
    temp_low = Column(Float)
    rain_total = Column(Float)
    humidity_high = Column(Float)
    humidity_low = Column(Float)
    wind_max = Column(Float)
    uv_high = Column(Float)
    pressure_max = Column(Float)
    pressure_min = Column(Float)

    def __repr__(self) -> str:
        return f"Weather: ({self.id_location}, {self.temp})"

    def __str__(self) -> str:
        return super().__str__()

    @staticmethod
    def write_weather(dict_weather_data):
        weather = Weather()
        weather.id_location = 1  # Cercedilla
        weather.date = datetime.now(pytz.timezone('Europe/Madrid')
                                    ).strftime("%Y-%m-%d %H:%M")
        weather.temp_high = float(dict_weather_data["metric"]["tempHigh"])
        weather.temp_low = float(dict_weather_data["metric"]["tempLow"])
        weather.rain_total = float(dict_weather_data["metric"]["precipTotal"])
        weather.humidity_high = float(dict_weather_data["humidityHigh"])
        weather.humidity_low = float(dict_weather_data["humidityLow"])
        weather.wind_max = float(dict_weather_data["metric"]["windgustHigh"])
        weather.uv_high = float(dict_weather_data["uvHigh"])
        weather.pressure_max = float(dict_weather_data["metric"]["pressureMax"])
        weather.pressure_min = float(dict_weather_data["metric"]["pressureMin"])

        db.session.add(weather)
        db.session.commit()
