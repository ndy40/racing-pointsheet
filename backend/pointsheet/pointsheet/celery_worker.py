import os

from celery import Celery


def _celery_collect_submodules(directory):
    submodules = []
    for root, dirs, files in os.walk(directory):
        if "__init__.py" in files:
            module_name = root.replace(os.path.sep, ".")
            submodules.append(module_name)
    return submodules


celery_task = Celery("pointsheet")
celery_task.config_from_object("pointsheet.celeryconfig")
celery_task.autodiscover_tasks(_celery_collect_submodules("modules"))
