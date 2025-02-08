import uuid

from modules.auth.exceptions import EventNotFoundException
from modules.event.dependencies import container
from modules.event.domain.entity import RaceResult, Event
from modules.event.domain.value_objects import DriverResult
from modules.event.repository import EventRepository
from pointsheet.celery_worker import celery_task


@celery_task.task
def say_hello():
    print("Hello world!!")


@celery_task.task(
    autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5}
)
def extract_race_result_from_file(event_id, schedule_id, file_path):
    repo = container[EventRepository]
    event: Event = repo.find_by_id(event_id)

    if not event:
        raise EventNotFoundException()

    # Perform AI extraction
    driver_result = DriverResult(
        driver_id=uuid.uuid4(),
        driver="Driver 1",
        position=1,
        best_lap="00:54.2345",
        total="01:00.2345",
        penalties=0,
        points=10,
        total_points=10,
    )
    result = RaceResult(
        schedule_id=schedule_id,
        result=[driver_result],
        upload_file=file_path,
        mark_down="""# looks like we have results""",
    )
    event.add_result(result)
    repo.update(event)
