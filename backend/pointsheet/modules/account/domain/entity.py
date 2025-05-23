from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from modules.account.domain.exceptions import (
    AlreadySignedUpException,
    AlreadyTeamMemberException,
    AlreadyInTeamException,
)
from pointsheet.domain.value_objects import TeamMember
from pointsheet.domain.entity import AggregateRoot
from pointsheet.domain.types import EntityId


class RaceEvent(BaseModel):
    event_id: EntityId
    title: str
    status: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    track: Optional[str] = None


class Team(AggregateRoot):
    name: str
    description: Optional[str] = None
    owner_id: EntityId  # Reference to User from auth module
    members: List[TeamMember] = []

    def add_member(self, driver_id: EntityId, role: str = "member") -> None:
        if any(member.driver_id == driver_id for member in self.members):
            raise AlreadyTeamMemberException(
                f"Driver {driver_id} is already a member of this team"
            )

        self.members.append(
            TeamMember(driver_id=driver_id, role=role, joined_at=datetime.now())
        )

    def remove_member(self, driver_id: EntityId) -> None:
        self.members = [
            member for member in self.members if member.driver_id != driver_id
        ]

    def is_member(self, driver_id: EntityId) -> bool:
        return any(member.driver_id == driver_id for member in self.members)

    def is_owner(self, user_id: EntityId) -> bool:
        return self.owner_id == user_id


class Driver(AggregateRoot):
    name: Optional[str] = None
    events: Optional[List[RaceEvent]] = None
    team_id: Optional[EntityId] = None  # Reference to team

    def join_event(self, event: RaceEvent):
        if any(
            existing_event.event_id == event.event_id for existing_event in self.events
        ):
            raise AlreadySignedUpException(
                f"User is already signed up for event {event.event_id}."
            )
        self.events.append(event)

    def join_team(self, team_id: EntityId):
        if self.team_id:
            raise AlreadyInTeamException(
                f"Driver is already a member of team {self.team_id}"
            )
        self.team_id = team_id

    def leave_team(self):
        self.team_id = None
