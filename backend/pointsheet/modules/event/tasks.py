from pointsheet.celery_worker import celery_tasks


@celery_tasks.task
def say_hello():
    print("Hello world!!")
