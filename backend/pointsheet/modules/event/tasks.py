from pointsheet.celery import app


@app.task
def say_hello():
    print("Hello world!!")
