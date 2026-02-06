"""Utils package - exports all utility functions"""

from .dice import roll_dice, roll_ability_score, parse_dice_notation, roll_from_notation
from .calculations import (
    calculate_modifier,
    calculate_proficiency_bonus,
    calculate_hp_from_cr,
    calculate_ac_from_cr,
    get_xp_by_cr,
)
from .formatters import format_modifier, pluralize, titlecase
from .validators import (
    validate_ability_score,
    validate_level,
    validate_challenge_rating,
    validate_dice_notation,
)

__all__ = [
    # Dice
    "roll_dice",
    "roll_ability_score",
    "parse_dice_notation",
    "roll_from_notation",
    # Calculations
    "calculate_modifier",
    "calculate_proficiency_bonus",
    "calculate_hp_from_cr",
    "calculate_ac_from_cr",
    "get_xp_by_cr",
    # Formatters
    "format_modifier",
    "pluralize",
    "titlecase",
    # Validators
    "validate_ability_score",
    "validate_level",
    "validate_challenge_rating",
    "validate_dice_notation",
]
