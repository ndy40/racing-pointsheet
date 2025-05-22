from pointsheet.models.account import Driver as DriverEntity
from pointsheet.repository import DataMapper

from .domain.entity import Driver


class UserMapper(DataMapper[DriverEntity, Driver]):
    def to_db_entity(self, instance: Driver) -> DriverEntity:
        return DriverEntity(
            id=instance.id,
            name=instance.name,
        )

    def to_domain_model(self, instance: DriverEntity) -> Driver:
        return Driver(
            id=instance.id,
            name=instance.name,
        )
