from pointsheet.db import get_session
from pointsheet.factories.event import SeriesFactory, EventFactory


def run():
    session = get_session()

    with session.begin():
        for i in range(0, 3):
            SeriesFactory(title=f"Home {i}")
            EventFactory()

        session.commit()
