import json
import logging

from flask import Blueprint, current_app, request

from modules.event.commands.create_series import CreateSeries
from modules.event.domain.entity import Series
from modules.event.queries.get_all_series import GetAllSeries
from modules.event.queries.get_series_by_id import GetSeriesById

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)

event_bp = Blueprint("event", __name__)


@event_bp.route("/series", methods=["GET"])
def fetch_all_series():
    result = current_app.application.execute(GetAllSeries())
    return [dict(item) for item in result]


@event_bp.route("/series", methods=["POST"])
def create_series():
    cmd = CreateSeries(**json.loads(request.data))
    current_app.application.execute(cmd)
    series: Series = current_app.application.execute(GetSeriesById(id=cmd.id))
    return series.model_dump()
