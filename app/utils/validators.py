"""Validation utilities for D&D game data"""


def validate_ability_score(score: int) -> bool:
    """
    Validate ability score is within valid range.
    
    Args:
        score: Ability score value
    
    Returns:
        True if valid (1-30), False otherwise
    """
    return 1 <= score <= 30


def validate_level(level: int) -> bool:
    """
    Validate character level is within valid range.
    
    Args:
        level: Character level
    
    Returns:
        True if valid (1-20), False otherwise
    """
    return 1 <= level <= 20


def validate_challenge_rating(cr: float) -> bool:
    """
    Validate challenge rating is a valid value.
    
    Args:
        cr: Challenge rating
    
    Returns:
        True if valid, False otherwise
    """
    valid_crs = {
        0, 0.125, 0.25, 0.5, 
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
        11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30
    }
    return cr in valid_crs


def validate_dice_notation(notation: str) -> bool:
    """
    Validate dice notation format.
    
    Args:
        notation: Dice notation string (e.g., "2d6+3")
    
    Returns:
        True if valid format, False otherwise
    """
    import re
    pattern = r'^\d+d\d+([+-]\d+)?$'
    return bool(re.match(pattern, notation))
