"""Item and equipment models"""

from enum import Enum
from pydantic import BaseModel


class ItemType(str, Enum):
    """Item types"""

    WEAPON = "Weapon"
    ARMOR = "Armor"
    POTION = "Potion"
    WONDROUS_ITEM = "Wondrous Item"
    WAND = "Wand"
    RING = "Ring"
    SCROLL = "Scroll"


class Rarity(str, Enum):
    """Item rarity"""

    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    VERY_RARE = "Very Rare"
    LEGENDARY = "Legendary"
    ARTIFACT = "Artifact"


class Item(BaseModel):
    """D&D 5e Item/Equipment"""

    id: int
    name: str
    type: ItemType
    category: str
    rarity: Rarity
    description: str
    cost: int  # in gold pieces
    weight: float
    properties: list[str]
    magic: bool
    attunement_required: bool

    # Weapon-specific fields
    damage: str | None = None
    damage_type: str | None = None

    # Armor-specific fields
    armor_class: int | None = None
