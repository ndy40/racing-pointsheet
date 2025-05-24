import os
import uuid

from lato import Command
from pydantic import ConfigDict
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from modules.event import event_module
from modules.event.repository import SeriesRepository
from modules.event.exceptions import SeriesNotFoundException
from pointsheet.config import config
from pointsheet.domain.types import EntityId


class UploadSeriesCoverImage(Command):
    series_id: EntityId
    file: FileStorage

    model_config = ConfigDict(arbitrary_types_allowed=True)


def rename_file(file_path):
    """Renames a file with a UUID while keeping its original extension."""
    directory, file_name = os.path.split(file_path)
    file_extension = os.path.splitext(file_name)[1]  # Extracts extension

    new_name = f"{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(directory, new_name)

    os.rename(file_path, new_path)
    return new_path


@event_module.handler(UploadSeriesCoverImage)
def handle_upload_series_cover_image(
    cmd: UploadSeriesCoverImage,
    repo: SeriesRepository,
):
    # Validate file extension
    file_name = secure_filename(cmd.file.filename)
    full_path = os.path.join(config.UPLOAD_FOLDER, file_name)
    file_location = config.file_store.save_file(full_path, cmd.file.read(), rename=True)

    # Find the series
    series = repo.find_by_id(cmd.series_id)
    if not series:
        raise SeriesNotFoundException()

    # Update the series with the cover image path
    series.cover_image = file_location
    repo.update(series)
