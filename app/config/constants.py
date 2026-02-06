"""D&D game constants and lookup tables"""

from app.models import Size

# Experience Points by Challenge Rating
XP_BY_CR = {
    0: 10,
    0.125: 25,
    0.25: 50,
    0.5: 100,
    1: 200,
    2: 450,
    3: 700,
    4: 1100,
    5: 1800,
    6: 2300,
    7: 2900,
    8: 3900,
    9: 5000,
    10: 5900,
    11: 7200,
    12: 8400,
    13: 10000,
    14: 11500,
    15: 13000,
    16: 15000,
    17: 18000,
    18: 20000,
    19: 22000,
    20: 25000,
}

# Hit Dice by Creature Size
HIT_DICE_BY_SIZE = {
    Size.TINY: 4,
    Size.SMALL: 6,
    Size.MEDIUM: 8,
    Size.LARGE: 10,
    Size.HUGE: 12,
    Size.GARGANTUAN: 20,
}

# Challenge Rating Options (including fractional CRs)
VALID_CHALLENGE_RATINGS = [0, 0.125, 0.25, 0.5] + list(range(1, 31))

# Proficiency Bonus by Level/CR
PROFICIENCY_BONUS_BY_LEVEL = {
    1: 2,
    2: 2,
    3: 2,
    4: 2,
    5: 3,
    6: 3,
    7: 3,
    8: 3,
    9: 4,
    10: 4,
    11: 4,
    12: 4,
    13: 5,
    14: 5,
    15: 5,
    16: 5,
    17: 6,
    18: 6,
    19: 6,
    20: 6,
    21: 7,
    22: 7,
    23: 7,
    24: 7,
    25: 8,
    26: 8,
    27: 8,
    28: 8,
    29: 9,
    30: 9,
}

# Base walking speed by size
BASE_SPEED_BY_SIZE = {
    Size.TINY: 20,
    Size.SMALL: 25,
    Size.MEDIUM: 30,
    Size.LARGE: 40,
    Size.HUGE: 50,
    Size.GARGANTUAN: 50,
}

# Legendary Action threshold
LEGENDARY_ACTION_MIN_CR = 10

# Special abilities threshold
SPECIAL_ABILITIES_MIN_CR = 2
