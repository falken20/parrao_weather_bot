import logging

from parrao_weather_bot import db
from parrao_weather_bot.models import Location

logging.basicConfig(level=logging.DEBUG)


def create_default_location() -> None:
    location = db.session.get(Location, 1)
    if not location:
        logging.info("Location default doesn't exist")
        db.session.add(Location(1, 'Cercedilla'))
        db.session.commit()
    else:
        logging.info(
            f"Location default {location.desc_location} already exists")


if __name__ == '__main__':
    # If not exists, create the tables
    logging.info("Creating tables if they not exist...")
    db.Base.metadata.create_all(db.engine)
    create_default_location()
    logging.info("DB is ok for working")
