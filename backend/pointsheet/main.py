import os
import csv
from importlib import import_module

import click
from alembic import command
from alembic.config import Config
from dotenv import load_dotenv

from pointsheet.db import get_session
from pointsheet.models.event import Track, Car, Game

debug = False

load_dotenv()

if os.environ.get("APP_ENV", "dev") != "prod":
    debug = True


alembic_cfg_path = os.path.join(os.path.dirname(__file__), "alembic.ini")
alembic_cfg = Config(alembic_cfg_path)


@click.group()
def app():
    pass


@app.command()
@click.option("--rev", default="head")
def migrate(rev):
    command.upgrade(alembic_cfg, rev)


@app.command("mkm", help="create new migration scripts")
@click.argument("msg")
@click.option("--autogenerate", default=True)
def make_migration(msg, autogenerate):
    command.revision(alembic_cfg, message=msg, autogenerate=autogenerate)


@app.command("run-server")
@click.option("--debug", default=True)
def run_server(debug):
    from pointsheet import create_app

    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=debug, load_dotenv=True)


@app.command()
def seed_data():
    module = import_module("pointsheet.seed_factories")
    if hasattr(module, "run"):
        getattr(module, "run")()


@app.command("load-tracks")
def load_tracks_command():
    load_tracks()


def load_tracks():
    csv_path = os.path.join(os.path.dirname(__file__), "data", "tracks.csv")

    session = next(get_session())

    with session.begin():
        with open(csv_path, "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                track = Track(**row)
                session.add(track)


@app.command("load-games")
def load_games():
    csv_path = os.path.join(os.path.dirname(__file__), "data", "games.csv")
    session = next(get_session())

    with session.begin():
        with open(csv_path, "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                game = Game(**row)
                session.add(game)


@app.command("load-cars")
def load_cars():
    csv_path = os.path.join(os.path.dirname(__file__), "data", "forza_cars.csv")
    session = next(get_session())

    with session.begin():
        with open(csv_path, "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                car = Car(**row)
                session.add(car)




if __name__ == "__main__":
    app()
