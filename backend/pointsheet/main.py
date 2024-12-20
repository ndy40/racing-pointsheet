import os
from importlib import import_module

import click
from alembic import command
from alembic.config import Config
from dotenv import load_dotenv

debug = False

load_dotenv()

if os.environ.get("APP_ENV", "dev") != "prod":
    debug = True


alembic_cfg_path = os.path.join(os.path.dirname(__file__), "alembic.ini")
alembic_cfg = Config(alembic_cfg_path)


@click.group()
def db():
    pass


@db.command()
@click.option("--rev", default="head")
def migrate(rev):
    command.upgrade(alembic_cfg, rev)


@db.command("mkm", help="create new migration scripts")
@click.argument("msg")
@click.option("--autogenerate", default=True)
def make_migration(msg, autogenerate):
    command.revision(alembic_cfg, message=msg, autogenerate=autogenerate)


@db.command("run-server")
@click.option("--debug", default=True)
def run_server(debug):
    from pointsheet import create_app

    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=debug, load_dotenv=True)


@db.command()
def seed_data():
    module = import_module("pointsheet.seed_factories")
    if hasattr(module, "run"):
        getattr(module, "run")()


if __name__ == "__main__":
    db()
