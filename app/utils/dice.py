"""Dice rolling utilities for D&D mechanics"""

import random


def roll_dice(num_dice: int, die_size: int, modifier: int = 0) -> int:
    """
    Roll dice and return total with modifier.
    
    Args:
        num_dice: Number of dice to roll
        die_size: Size of each die (e.g., 6 for d6, 20 for d20)
        modifier: Modifier to add to the total
    
    Returns:
        Total of all dice rolls plus modifier
    
    Example:
        roll_dice(2, 6, 3)  # Rolls 2d6+3
    """
    rolls = [random.randint(1, die_size) for _ in range(num_dice)]
    return sum(rolls) + modifier


def roll_ability_score() -> int:
    """
    Roll 4d6, drop lowest die (standard D&D ability score method).
    
    Returns:
        Ability score between 3 and 18
    """
    rolls = [random.randint(1, 6) for _ in range(4)]
    rolls.remove(min(rolls))
    return sum(rolls)


def parse_dice_notation(notation: str) -> tuple[int, int, int]:
    """
    Parse dice notation string (e.g., "2d6+3") into components.
    
    Args:
        notation: Dice notation string (e.g., "2d6+3", "1d20", "3d8-2")
    
    Returns:
        Tuple of (num_dice, die_size, modifier)
    
    Example:
        parse_dice_notation("2d6+3")  # Returns (2, 6, 3)
    """
    modifier = 0
    
    # Handle modifier
    if '+' in notation:
        dice_part, mod_part = notation.split('+')
        modifier = int(mod_part)
    elif '-' in notation:
        dice_part, mod_part = notation.split('-')
        modifier = -int(mod_part)
    else:
        dice_part = notation
    
    # Parse dice
    num_dice, die_size = dice_part.split('d')
    return int(num_dice), int(die_size), modifier


def roll_from_notation(notation: str) -> int:
    """
    Roll dice from notation string.
    
    Args:
        notation: Dice notation string (e.g., "2d6+3")
    
    Returns:
        Total rolled value
    
    Example:
        roll_from_notation("2d6+3")  # Rolls 2d6+3
    """
    num_dice, die_size, modifier = parse_dice_notation(notation)
    return roll_dice(num_dice, die_size, modifier)
