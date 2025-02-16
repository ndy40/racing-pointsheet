from lato import TransactionContext

from modules.auth.exceptions import EventNotFoundException
from modules.event.dependencies import container
from modules.event.domain.entity import Event
from modules.event.events import RaceResultUploaded
from modules.event.repository import EventRepository
from modules.event.use_case.extract_race_result import ExtractRaceResult
from modules.event.use_case.save_race_result import SaveRaceResult
from pointsheet.celery_worker import celery_task


@celery_task.task(retry_backoff=True, retry_kwargs={"max_retries": 2})
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

    output = ExtractRaceResult(file_path).execute()
    save_result_op = SaveRaceResult(repo)

    save_result_op(event.id, schedule_id, output)

    TransactionContext().publish(
        RaceResultUploaded(event_id=event_id, schedule_id=schedule_id)
    )
