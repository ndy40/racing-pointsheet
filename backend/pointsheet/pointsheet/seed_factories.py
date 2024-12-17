import logging

from pointsheet.db import get_session
from pointsheet.factories.event import SeriesFactory, EventFactory

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)


def run():
    session = get_session()

    with session.begin():
        for i in range(0, 3):
            SeriesFactory(title=f"Series {i}")
            EventFactory()

        session.commit()
