"""Spell-related models and enums"""

from enum import Enum
from pydantic import BaseModel


class SpellSchool(str, Enum):
    """Schools of magic"""

    ABJURATION = "Abjuration"
    CONJURATION = "Conjuration"
    DIVINATION = "Divination"
    ENCHANTMENT = "Enchantment"
    EVOCATION = "Evocation"
    ILLUSION = "Illusion"
    NECROMANCY = "Necromancy"
    TRANSMUTATION = "Transmutation"


class SpellComponent(str, Enum):
    """Spell components"""

    VERBAL = "V"
    SOMATIC = "S"
    MATERIAL = "M"


class Spell(BaseModel):
    """D&D 5e Spell"""

    id: int
    name: str
    level: int  # 0 = cantrip, 1-9 = spell level
    school: SpellSchool
    casting_time: str
    range: str
    components: list[SpellComponent]
    material: str | None = None
    duration: str
    concentration: bool
    ritual: bool
    description: str
    higher_levels: str | None = None
    classes: list[str]
