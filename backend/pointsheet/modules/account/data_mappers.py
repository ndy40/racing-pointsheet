from pointsheet.models import Driver
from pointsheet.repository import DataMapper

from .domain.entity import Driver as DriverModel


class DriverMapper(DataMapper[Driver, DriverModel]):
    def to_db_entity(self, instance: DriverModel) -> Driver:
        return Driver(
            id=instance.id,
            name=instance.name,
        )

    def to_domain_model(self, instance: Driver) -> DriverModel:
        return DriverModel(
            id=instance.id,
            name=instance.name,
        )
