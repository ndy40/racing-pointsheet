from typing import AnyStr

from lato import Query


class GetAllSeries(Query): ...


class GetSeriesById(Query):
    id: AnyStr
