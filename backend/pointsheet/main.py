import os
import csv
from importlib import import_module

import click
from alembic import command
from alembic.config import Config
from dotenv import load_dotenv
from sqlalchemy import text

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


@app.command(help="migrate database to latest revision")
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


@app.group()
def seed_data():
    pass


@seed_data.command("load-tracks", help="Load tracks from CSV file")
def load_tracks():
    csv_path = os.path.join(os.path.dirname(__file__), "data", "tracks.csv")

    session = next(get_session())

    with session.begin():
        with open(csv_path, "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                track = Track(**row)
                session.add(track)


@seed_data.command("load-games", help="Load games from CSV file")
def load_games():
    csv_path = os.path.join(os.path.dirname(__file__), "data", "games.csv")
    session = next(get_session())

    with session.begin():
        with open(csv_path, "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                game = Game(**row)
                session.add(game)


@seed_data.command("load-cars", help="Load cars from CSV file")
def load_cars():
    csv_path = os.path.join(os.path.dirname(__file__), "data", "forza_cars.csv")
    session = next(get_session())

    with session.begin():
        with open(csv_path, "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                car = Car(**row)
                session.add(car)

@app.command("create-car-fts", help="Create and populate car full-text search index")
def create_car_full_text_search_index():
    session = next(get_session())
    with session.begin():
        session.execute(text("""
            DROP TABLE IF EXISTS car_fts;
        """))

        session.execute(text("""
            DROP TRIGGER IF EXISTS car_ai;
        """))

        session.execute(text("""
            DROP TRIGGER IF EXISTS car_ad;
        """))

        session.execute(text("""
            DROP TRIGGER IF EXISTS car_au;
        """))

        session.execute(text("""
            CREATE VIRTUAL TABLE car_fts USING fts5(
                model, 
                year,
                content='car',
                content_rowid='id'
            );
        """))

        session.execute(text("""
            INSERT INTO car_fts(rowid, model, year)
            SELECT id, model, year
            FROM cars;
        """))

        session.execute(text("""
            CREATE TRIGGER car_ai AFTER INSERT ON cars BEGIN
                INSERT INTO car_fts(rowid, model, year)
                VALUES (new.id, new.model, new.year);
            END;
        """))

        session.execute(text("""
            CREATE TRIGGER car_ad AFTER DELETE ON cars BEGIN
                DELETE FROM car_fts WHERE rowid = old.id;
            END;
        """))

        session.execute(text("""
            CREATE TRIGGER car_au AFTER UPDATE ON cars BEGIN
                UPDATE car_fts SET 
                    model = new.model,
                    year = new.year
                WHERE rowid = old.id;
            END;
        """))



if __name__ == "__main__":
    app()
