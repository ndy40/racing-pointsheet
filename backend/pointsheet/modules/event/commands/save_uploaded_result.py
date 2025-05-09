import os

from lato import Command, TransactionContext
from pydantic import ConfigDict
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from modules.auth.exceptions import EventNotFoundException
from modules.event import event_module
from modules.event.repository import EventRepository
from modules.event.tasks import extract_race_result_from_file
from pointsheet.domain import EntityId
from pointsheet.storage import FileStore


class UploadRaceResult(Command):
    event_id: EntityId
    schedule_id: int
    file: FileStorage

    model_config = ConfigDict(arbitrary_types_allowed=True)


@event_module.handler(UploadRaceResult)
def handle_save_uploaded_result(
    cmd: UploadRaceResult,
    ctx: TransactionContext,
    file_store: FileStore,
    config,
    repo: EventRepository,
):
    # validate file extension
    file_name = secure_filename(cmd.file.filename)
    full_path = os.path.join(config.UPLOAD_FOLDER, file_name)
    file_location = file_store.save_file(full_path, cmd.file.read())

    event = repo.find_by_id(cmd.event_id)

    if not event:
        raise EventNotFoundException()

    extract_race_result_from_file.delay(cmd.event_id, cmd.schedule_id, file_location)
