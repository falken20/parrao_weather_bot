import logging

import db
from models import Location, Weather


if __name__ == '__main__':
    # If not exists, create the tables
    logging.info("Creating tables if they not exist...")
    db.Base.metadata.create_all(db.engine)
    logging.info("Tables created succesfully")