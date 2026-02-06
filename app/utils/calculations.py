"""Calculation utilities for D&D game mechanics"""

from app.config.constants import XP_BY_CR, HIT_DICE_BY_SIZE
from app.models import Size


def calculate_modifier(ability_score: int) -> int:
    """
    Calculate ability modifier from ability score.
    
    Args:
        ability_score: Ability score value (typically 1-30)
    
    Returns:
        Ability modifier
    
    Example:
        calculate_modifier(16)  # Returns +3
    """
    return (ability_score - 10) // 2


def calculate_proficiency_bonus(level: int) -> int:
    """
    Calculate proficiency bonus based on character/monster level.
    
    Args:
        level: Character or monster level (1-20)
    
    Returns:
        Proficiency bonus
    """
    return 2 + ((level - 1) // 4)


def calculate_hp_from_cr(challenge_rating: float, size: Size, constitution_modifier: int = 0) -> tuple[int, str]:
    """
    Calculate HP and hit dice based on CR and size.
    
    Args:
        challenge_rating: Monster challenge rating
        size: Monster size (affects hit die size)
        constitution_modifier: Constitution modifier per die
    
    Returns:
        Tuple of (hit_points, hit_dice_notation)
    
    Example:
        calculate_hp_from_cr(5.0, Size.LARGE, 2)  # Returns (95, "10d10+20")
    """
    import random
    
    die_size = HIT_DICE_BY_SIZE[size]
    num_dice = max(1, int(challenge_rating * 3) + random.randint(1, 6))
    
    if constitution_modifier == 0:
        constitution_modifier = int(challenge_rating)
    
    # Calculate HP: (num_dice * (die_size / 2 + 0.5)) + (num_dice * con_bonus)
    average_roll = (die_size / 2) + 0.5
    hit_points = int((num_dice * average_roll) + (num_dice * constitution_modifier))
    hit_dice = f"{num_dice}d{die_size}+{num_dice * constitution_modifier}"
    
    return hit_points, hit_dice


def calculate_ac_from_cr(challenge_rating: float) -> int:
    """
    Calculate appropriate AC based on challenge rating.
    
    Args:
        challenge_rating: Monster challenge rating
    
    Returns:
        Armor class value
    """
    # Base AC 10 + CR scaling
    return min(10 + int(challenge_rating * 0.75), 25)


def get_xp_by_cr(challenge_rating: float) -> int:
    """
    Get experience points for a given challenge rating.
    
    Args:
        challenge_rating: Monster challenge rating
    
    Returns:
        Experience points value
    """
    return XP_BY_CR.get(challenge_rating, 0)
