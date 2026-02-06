"""Monster-related models and enums"""

from enum import Enum
from pydantic import BaseModel

from .common import Alignment, Size, Stats


class MonsterType(str, Enum):
    """Monster types"""

    ABERRATION = "Aberration"
    BEAST = "Beast"
    CELESTIAL = "Celestial"
    CONSTRUCT = "Construct"
    DRAGON = "Dragon"
    ELEMENTAL = "Elemental"
    FEY = "Fey"
    FIEND = "Fiend"
    GIANT = "Giant"
    HUMANOID = "Humanoid"
    MONSTROSITY = "Monstrosity"
    OOZE = "Ooze"
    PLANT = "Plant"
    UNDEAD = "Undead"


class DamageType(str, Enum):
    """Damage types"""

    ACID = "Acid"
    BLUDGEONING = "Bludgeoning"
    COLD = "Cold"
    FIRE = "Fire"
    FORCE = "Force"
    LIGHTNING = "Lightning"
    NECROTIC = "Necrotic"
    PIERCING = "Piercing"
    POISON = "Poison"
    PSYCHIC = "Psychic"
    RADIANT = "Radiant"
    SLASHING = "Slashing"
    THUNDER = "Thunder"


class Action(BaseModel):
    """Monster action (attack, spell, ability)"""

    name: str
    description: str
    attack_bonus: int | None = None
    damage_dice: str | None = None  # e.g., "2d6+4"
    damage_type: DamageType | None = None


class Monster(BaseModel):
    """D&D 5e Monster stat block"""

    id: int
    name: str
    size: Size
    type: MonsterType
    alignment: Alignment

    # Defense
    armor_class: int
    hit_points: int
    hit_dice: str  # e.g., "8d10+16"

    # Speed
    speed: dict[str, int]  # e.g., {"walk": 30, "fly": 60, "swim": 30}

    # Ability scores
    stats: Stats

    # Skills & Senses
    saving_throws: dict[str, int] | None = None  # e.g., {"dexterity": 5, "wisdom": 3}
    skills: dict[str, int] | None = None  # e.g., {"perception": 4, "stealth": 6}
    damage_resistances: list[DamageType] | None = None
    damage_immunities: list[DamageType] | None = None
    condition_immunities: list[str] | None = None
    senses: dict[str, int] | None = (
        None  # e.g., {"darkvision": 60, "passive_perception": 14}
    )
    languages: list[str] | None = None

    # Combat Rating
    challenge_rating: float  # 0, 0.125, 0.25, 0.5, 1, 2, etc.
    experience_points: int

    # Special Abilities
    special_abilities: list[Action] | None = None
    actions: list[Action]
    legendary_actions: list[Action] | None = None
    reactions: list[Action] | None = None
