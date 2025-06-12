from pointsheet.models.account import Driver as DriverEntity, Team as TeamEntity
from pointsheet.repository import DataMapper

from .domain.entity import Driver, Team


class DriverMapper(DataMapper[DriverEntity, Driver]):
    def to_db_entity(self, instance: Driver) -> DriverEntity:
        return DriverEntity(
            id=instance.id,
            name=instance.name,
            team_id=instance.team_id,
            role=instance.role,
        )

    def to_domain_model(self, instance: DriverEntity) -> Driver:
        return Driver(
            id=instance.id,
            name=instance.name,
            team_id=instance.team_id,
            role=instance.role
        )


class TeamMapper(DataMapper[TeamEntity, Team]):
    def to_db_entity(self, instance: Team) -> TeamEntity:
        return TeamEntity(
            id=instance.id,
            name=instance.name,
            description=instance.description,
            owner_id=instance.owner_id,
            members=instance.members,
        )

    def to_domain_model(self, instance: TeamEntity) -> Team:
        return Team(
            id=instance.id,
            name=instance.name,
            description=instance.description,
            owner_id=instance.owner_id,
            members=instance.members,
        )
