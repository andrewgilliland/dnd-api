from pydantic import BaseModel, Field
from enum import Enum


class Class(str, Enum):
    """D&D 5e character classes"""

    BARBARIAN = "Barbarian"
    BARD = "Bard"
    CLERIC = "Cleric"
    DRUID = "Druid"
    FIGHTER = "Fighter"
    MONK = "Monk"
    PALADIN = "Paladin"
    RANGER = "Ranger"
    ROGUE = "Rogue"
    SORCERER = "Sorcerer"
    WARLOCK = "Warlock"
    WIZARD = "Wizard"


class Stats(BaseModel):
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int


class Character(BaseModel):
    id: int
    name: str
    race: str
    class_: Class = Field(alias="class")  # 'class' is a reserved keyword
    alignment: str
    description: str
    stats: Stats

    model_config = {
        "populate_by_name": True  # Allows both 'class' and 'class_' to work
    }


class CharactersResponse(BaseModel):
    characters: list[Character]
