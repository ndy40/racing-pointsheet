import os
from pathlib import Path

from flask import Flask, render_template, url_for

from pointsheet.config import Config

# from pointsheet.db import Session

root_dir = os.path.join(Path(__file__).parent.parent)

static_directory = os.path.join(root_dir, 'static')
template_directory = os.path.join(root_dir, 'templates')

config = Config()

def create_app(test_config=None):
    app = Flask(__name__, static_folder=static_directory, template_folder=template_directory,)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'point_sheets.db.sqlite')
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('index.html');

    @app.route('/hello')
    def hello():
        return "Hello world"

    # @app.teardown_appcontext
    # def remove_db_session():
    #     Session.remove()

    return app