import os

from celery import Celery
from pointsheet.config import Config

config = Config()


# Function to collect all submodules under 'modules'
def collect_submodules(directory):
    submodules = []
    for root, dirs, files in os.walk(directory):
        if "__init__.py" in files:
            module_name = root.replace(os.path.sep, ".")
            submodules.append(module_name)
    return submodules


# Collect all submodules under 'modules'
submodules = collect_submodules("modules")

app = Celery("pointsheet", broker=config.QUEUE_BROKER, backend=config.BROKER_BACKEND)

app.autodiscover_tasks(packages=submodules)
