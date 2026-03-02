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


class SkillType(str, Enum):
    """D&D 5e skill types"""

    ACROBATICS = "acrobatics"
    ANIMAL_HANDLING = "animal_handling"
    ARCANA = "arcana"
    ATHLETICS = "athletics"
    DECEPTION = "deception"
    HISTORY = "history"
    INSIGHT = "insight"
    INTIMIDATION = "intimidation"
    INVESTIGATION = "investigation"
    MEDICINE = "medicine"
    NATURE = "nature"
    PERCEPTION = "perception"
    PERFORMANCE = "performance"
    PERSUASION = "persuasion"
    RELIGION = "religion"
    SLEIGHT_OF_HAND = "sleight_of_hand"
    STEALTH = "stealth"
    SURVIVAL = "survival"


class HitPoints(BaseModel):
    """Character hit point tracking"""

    current: int
    max: int
    temp: int | None = None


class Proficiencies(BaseModel):
    """Character proficiencies and training"""

    armor: list[str] | None = None
    weapons: list[str] | None = None
    tools: list[str] | None = None
    languages: list[str] | None = None


class CharacterAction(BaseModel):
    """Character action or attack entry"""

    name: str
    description: str
    attack_bonus: int | None = None
    damage: str | None = None
    range: str | None = None
    notes: str | None = None


class CharacterSkill(BaseModel):
    """Character skill bonus details"""

    skill: SkillType
    bonus: int
    proficient: bool = False


class Character(BaseModel):
    """D&D 5e Character"""

    id: int
    name: str
    race: Race
    class_: Class = Field(alias="class")  # 'class' is a reserved keyword
    alignment: Alignment
    description: str
    stats: Stats
    level: int | None = None
    proficiency_bonus: int | None = None
    initiative: int | None = None
    armor_class: int | None = None
    speed: dict[str, int] | None = None
    hit_points: HitPoints | None = None
    saving_throws: dict[str, int] | None = None
    saving_throw_proficiencies: list[str] | None = None
    skills: list[CharacterSkill] | None = None
    skill_proficiencies: list[str] | None = None
    passive_scores: dict[str, int] | None = None
    senses: dict[str, int] | None = None
    defenses: list[str] | None = None
    condition_immunities: list[str] | None = None
    proficiencies: Proficiencies | None = None
    actions: list[CharacterAction] | None = None

    model_config = {
        "populate_by_name": True  # Allows both 'class' and 'class_' to work
    }
