from pointsheet import create_app

flask_app = create_app()
celery_tasks = flask_app.extensions["celery"]
