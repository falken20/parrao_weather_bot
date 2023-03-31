from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
import pytz  # Work with time zones

from parrao_weather_bot import db


class Location(db.Base):
    __tablename__ = 't_location'

    id_location = Column(Integer, primary_key=True)
    desc_location = Column(String, nullable=False)

    def __init__(self, id_location, desc_location):
        self.id_location = id_location
        self.desc_location = desc_location

    def __repr__(self) -> str:
        return f"Location({self.id_location}, {self.desc_location}"

    def __str__(self) -> str:
        return self.desc_location


class Weather(db.Base):
    __tablename__ = 't_weather'

    id = Column(Integer, primary_key=True)
    id_location = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    temp = Column(Float)
    rain = Column(Float)
    humidity = Column(Float)
    wind = Column(Float)
    uv = Column(Float)
    pressure = Column(Float)

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
        weather.temp = float(dict_weather_data["metric"]["temp"])
        weather.rain = float(dict_weather_data["metric"]["precipTotal"])
        weather.humidity = float(dict_weather_data["humidity"])
        weather.wind = float(dict_weather_data["metric"]["windSpeed"])
        weather.uv = float(dict_weather_data["uv"])
        weather.pressure = float(dict_weather_data["metric"]["pressure"])

        db.session.add(weather)
        db.session.commit()
