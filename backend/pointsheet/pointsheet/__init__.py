import os

from flask import Flask



def create_app(test_config=None):
    app = Flask(__name__)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return 'hello world'

    return app