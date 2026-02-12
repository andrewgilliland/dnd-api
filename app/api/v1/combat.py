"""Combat calculator endpoints for attack rolls, damage, and saving throws"""

from fastapi import APIRouter, Body

from app.models.combat import (
    AttackRollRequest,
    AttackRollResponse,
    DamageRollRequest,
    DamageRollResponse,
    SavingThrowRequest,
    SavingThrowResponse,
    CombatCalculatorRequest,
    CombatCalculatorResponse,
)
from app.services.combat_service import (
    calculate_attack_roll,
    calculate_damage_roll,
    calculate_saving_throw,
    calculate_full_combat,
)

router = APIRouter()


@router.post("/attack-roll", response_model=AttackRollResponse)
def roll_attack(
    request: AttackRollRequest = Body(
        ...,
        examples=[
            {"attack_bonus": 5, "armor_class": 15, "advantage": "normal"},
            {"attack_bonus": 7, "armor_class": 18, "advantage": "advantage"},
            {"attack_bonus": 3, "armor_class": 12, "advantage": "disadvantage"},
        ],
    ),
):
    """
    Calculate an attack roll against a target's AC.

    Features:
    - Supports advantage/disadvantage
    - Automatically detects critical hits (natural 20)
    - Automatically detects critical misses (natural 1)
    - Returns whether the attack hits

    Parameters:
    - attack_bonus: Total attack bonus (ability mod + proficiency + magic items)
    - armor_class: Target's AC
    - advantage: "normal", "advantage", or "disadvantage"

    Returns:
    - Roll details including hit/miss, critical status
    """
    return calculate_attack_roll(request)


@router.post("/damage-roll", response_model=DamageRollResponse)
def roll_damage(
    request: DamageRollRequest = Body(
        ...,
        examples=[
            {"damage_dice": "2d6+3", "damage_type": "slashing", "critical_hit": False},
            {"damage_dice": "1d8+5", "damage_type": "piercing", "critical_hit": True},
            {"damage_dice": "3d6", "damage_type": "fire", "critical_hit": False},
        ],
    ),
):
    """
    Calculate damage from a weapon or spell.

    Features:
    - Parses dice notation (e.g., "2d6+3", "1d8+5")
    - Doubles dice on critical hits (not the modifier)
    - Shows individual dice rolls
    - Specifies damage type

    Parameters:
    - damage_dice: Dice notation string (e.g., "2d6+3")
    - damage_type: Type of damage (slashing, fire, etc.)
    - critical_hit: Whether this is a critical hit

    Returns:
    - Individual rolls, modifier, total damage, and type
    """
    return calculate_damage_roll(request)


@router.post("/saving-throw", response_model=SavingThrowResponse)
def roll_saving_throw(
    request: SavingThrowRequest = Body(
        ...,
        examples=[
            {
                "ability_modifier": 2,
                "proficiency_bonus": 3,
                "dc": 15,
                "advantage": "normal",
            },
            {
                "ability_modifier": -1,
                "proficiency_bonus": 0,
                "dc": 18,
                "advantage": "disadvantage",
            },
        ],
    ),
):
    """
    Calculate a saving throw against a DC.

    Features:
    - Supports advantage/disadvantage
    - Includes proficiency bonus if proficient
    - Detects natural 20s and natural 1s
    - Returns success/failure

    Parameters:
    - ability_modifier: Ability score modifier (e.g., +2 for 14 DEX)
    - proficiency_bonus: Proficiency bonus if proficient in this save
    - dc: Difficulty class to beat
    - advantage: "normal", "advantage", or "disadvantage"

    Returns:
    - Roll details including success/failure
    """
    return calculate_saving_throw(request)


@router.post("/combat", response_model=CombatCalculatorResponse)
def calculate_combat(
    request: CombatCalculatorRequest = Body(
        ...,
        examples=[
            {
                "attack_bonus": 5,
                "armor_class": 15,
                "damage_dice": "2d6+3",
                "damage_type": "slashing",
                "advantage": "normal",
            },
            {
                "attack_bonus": 7,
                "armor_class": 18,
                "damage_dice": "1d8+5",
                "damage_type": "piercing",
                "advantage": "advantage",
            },
        ],
    ),
):
    """
    Calculate a full combat turn (attack roll + damage if hit).

    This is a convenience endpoint that combines attack and damage rolls.
    If the attack misses, no damage is calculated.
    If the attack crits, damage dice are automatically doubled.

    Features:
    - Rolls attack with advantage/disadvantage
    - Automatically calculates damage if hit
    - Doubles dice on critical hits
    - Returns complete combat results

    Parameters:
    - attack_bonus: Total attack bonus
    - armor_class: Target's AC
    - damage_dice: Damage dice notation
    - damage_type: Type of damage
    - advantage: "normal", "advantage", or "disadvantage"

    Returns:
    - Full combat results including attack and damage (if applicable)
    """
    return calculate_full_combat(request)


@router.get("")
def combat_calculator_info():
    """
    Information about the combat calculator endpoints.

    Returns available calculations and their uses.
    """
    return {
        "description": "D&D 5e Combat Calculator",
        "endpoints": {
            "POST /combat/attack-roll": "Roll an attack (d20 + modifier) against AC",
            "POST /combat/damage-roll": "Roll damage dice with optional critical hit",
            "POST /combat/saving-throw": "Roll a saving throw against a DC",
            "POST /combat/combat": "Full combat calculation (attack + damage)",
        },
        "features": [
            "Advantage/disadvantage support",
            "Critical hit detection",
            "Automatic damage doubling on crits",
            "Flexible dice notation parsing",
            "All D&D 5e damage types",
        ],
    }
