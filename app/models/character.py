"""Character-related models and enums"""

from enum import Enum
from pydantic import BaseModel, Field

from .common import Alignment, Stats


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


class Race(str, Enum):
    """D&D 5e character races"""

    DRAGONBORN = "Dragonborn"
    DWARF = "Dwarf"
    ELF = "Elf"
    GNOME = "Gnome"
    HALF_ELF = "Half-Elf"
    HALF_ORC = "Half-Orc"
    HALFLING = "Halfling"
    HUMAN = "Human"
    TIEFLING = "Tiefling"


class Character(BaseModel):
    """D&D 5e Character"""

    id: int
    name: str
    race: Race
    class_: Class = Field(alias="class")  # 'class' is a reserved keyword
    alignment: Alignment
    description: str
    stats: Stats

    model_config = {
        "populate_by_name": True  # Allows both 'class' and 'class_' to work
    }
