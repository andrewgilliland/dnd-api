"""Combat-related models for attack rolls, damage, and saving throws"""

from enum import Enum
from pydantic import BaseModel, Field


class AdvantageType(str, Enum):
    """Type of advantage/disadvantage on a roll"""

    NORMAL = "normal"
    ADVANTAGE = "advantage"
    DISADVANTAGE = "disadvantage"


class DamageType(str, Enum):
    """Types of damage in D&D 5e"""

    ACID = "acid"
    BLUDGEONING = "bludgeoning"
    COLD = "cold"
    FIRE = "fire"
    FORCE = "force"
    LIGHTNING = "lightning"
    NECROTIC = "necrotic"
    PIERCING = "piercing"
    POISON = "poison"
    PSYCHIC = "psychic"
    RADIANT = "radiant"
    SLASHING = "slashing"
    THUNDER = "thunder"


class SavingThrowAbility(str, Enum):
    """Ability scores for saving throws"""

    STRENGTH = "strength"
    DEXTERITY = "dexterity"
    CONSTITUTION = "constitution"
    INTELLIGENCE = "intelligence"
    WISDOM = "wisdom"
    CHARISMA = "charisma"


class AttackRollRequest(BaseModel):
    """Request model for attack roll calculation"""

    attack_bonus: int = Field(
        ...,
        description="Total attack bonus (ability modifier + proficiency + magic items)",
    )
    armor_class: int = Field(..., ge=1, description="Target's armor class")
    advantage: AdvantageType = Field(
        default=AdvantageType.NORMAL, description="Advantage, disadvantage, or normal"
    )


class AttackRollResponse(BaseModel):
    """Response model for attack roll calculation"""

    roll: int = Field(
        ..., description="The d20 roll result (or highest/lowest for advantage)"
    )
    second_roll: int | None = Field(
        default=None, description="Second d20 roll if advantage/disadvantage"
    )
    attack_bonus: int = Field(..., description="Attack bonus applied")
    total: int = Field(..., description="Total attack roll (roll + bonus)")
    armor_class: int = Field(..., description="Target armor class")
    hit: bool = Field(..., description="Whether the attack hits")
    critical_hit: bool = Field(
        ..., description="Whether it's a critical hit (natural 20)"
    )
    critical_miss: bool = Field(
        ..., description="Whether it's a critical miss (natural 1)"
    )
    advantage: AdvantageType = Field(..., description="Type of advantage used")


class DamageRollRequest(BaseModel):
    """Request model for damage roll calculation"""

    damage_dice: str = Field(
        ..., description="Damage dice notation (e.g., '2d6+3', '1d8+5')"
    )
    damage_type: DamageType = Field(..., description="Type of damage")
    critical_hit: bool = Field(
        default=False,
        description="Whether this is a critical hit (doubles damage dice)",
    )


class DamageRollResponse(BaseModel):
    """Response model for damage roll calculation"""

    rolls: list[int] = Field(..., description="Individual dice roll results")
    modifier: int = Field(..., description="Damage modifier")
    total: int = Field(..., description="Total damage dealt")
    damage_type: DamageType = Field(..., description="Type of damage")
    critical_hit: bool = Field(..., description="Whether this was a critical hit")


class SavingThrowRequest(BaseModel):
    """Request model for saving throw calculation"""

    ability_modifier: int = Field(..., description="Ability modifier for the save")
    proficiency_bonus: int = Field(
        default=0, ge=0, description="Proficiency bonus if proficient in this save"
    )
    dc: int = Field(..., ge=1, description="Difficulty class to beat")
    advantage: AdvantageType = Field(
        default=AdvantageType.NORMAL, description="Advantage, disadvantage, or normal"
    )


class SavingThrowResponse(BaseModel):
    """Response model for saving throw calculation"""

    roll: int = Field(
        ..., description="The d20 roll result (or highest/lowest for advantage)"
    )
    second_roll: int | None = Field(
        default=None, description="Second d20 roll if advantage/disadvantage"
    )
    ability_modifier: int = Field(..., description="Ability modifier applied")
    proficiency_bonus: int = Field(..., description="Proficiency bonus applied")
    total: int = Field(..., description="Total saving throw (roll + modifiers)")
    dc: int = Field(..., description="Difficulty class")
    success: bool = Field(..., description="Whether the save succeeded")
    natural_20: bool = Field(..., description="Whether it's a natural 20")
    natural_1: bool = Field(..., description="Whether it's a natural 1")
    advantage: AdvantageType = Field(..., description="Type of advantage used")


class CombatCalculatorRequest(BaseModel):
    """Request model for full combat calculation (attack + damage)"""

    attack_bonus: int = Field(..., description="Total attack bonus")
    armor_class: int = Field(..., ge=1, description="Target's armor class")
    damage_dice: str = Field(..., description="Damage dice notation (e.g., '2d6+3')")
    damage_type: DamageType = Field(..., description="Type of damage")
    advantage: AdvantageType = Field(
        default=AdvantageType.NORMAL, description="Advantage, disadvantage, or normal"
    )


class CombatCalculatorResponse(BaseModel):
    """Response model for full combat calculation"""

    attack: AttackRollResponse = Field(..., description="Attack roll details")
    damage: DamageRollResponse | None = Field(
        default=None, description="Damage roll details (only if hit)"
    )
