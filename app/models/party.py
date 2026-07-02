"""Party-related models for D&D campaigns"""

from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


class PartyRole(str, Enum):
    """Party member roles"""

    TANK = "tank"
    SUPPORT = "support"
    HEALER = "healer"
    SCOUT = "scout"
    FACE = "face"
    CASTER = "caster"
    STRIKER = "striker"
    CONTROLLER = "controller"
    CUSTOM = "custom"


class PartyStatus(str, Enum):
    """Party status"""

    ACTIVE = "active"
    ARCHIVED = "archived"


class PartyMember(BaseModel):
    """A member of a party"""

    model_config = ConfigDict(populate_by_name=True)

    character_id: int = Field(alias="characterId")
    role: PartyRole | None = None
    is_leader: bool = Field(default=False, alias="isLeader")
    marching_order: int = Field(alias="marchingOrder")
    joined_at: str = Field(alias="joinedAt")


class CreatePartyMember(BaseModel):
    """Request model for creating a party member (no joinedAt required)"""

    model_config = ConfigDict(populate_by_name=True)

    character_id: int = Field(alias="characterId")
    role: PartyRole | None = None
    is_leader: bool = Field(default=False, alias="isLeader")
    marching_order: int = Field(alias="marchingOrder")


class Party(BaseModel):
    """A D&D party/adventuring group"""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    created_by_user_id: str = Field(alias="createdByUserId")
    status: PartyStatus
    members: list[PartyMember]
    notes: str | None = None
    tags: list[str] | None = None
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")


class CreatePartyRequest(BaseModel):
    """Request to create a new party"""

    model_config = ConfigDict(populate_by_name=True)

    name: str
    members: list[CreatePartyMember]
    notes: str | None = None
    tags: list[str] | None = None
