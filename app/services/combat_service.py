"""Service for combat calculations including attacks, damage, and saving throws"""

import random
from app.models.combat import (
    AdvantageType,
    AttackRollRequest,
    AttackRollResponse,
    DamageRollRequest,
    DamageRollResponse,
    SavingThrowRequest,
    SavingThrowResponse,
    CombatCalculatorRequest,
    CombatCalculatorResponse,
)
from app.utils.dice import parse_dice_notation


def roll_d20_with_advantage(advantage: AdvantageType) -> tuple[int, int | None]:
    """
    Roll a d20 with advantage, disadvantage, or normal.

    Args:
        advantage: Type of advantage on the roll

    Returns:
        Tuple of (primary_roll, second_roll)
        - For normal: (roll, None)
        - For advantage/disadvantage: (selected_roll, other_roll)
    """
    roll1 = random.randint(1, 20)

    if advantage == AdvantageType.NORMAL:
        return roll1, None

    roll2 = random.randint(1, 20)

    if advantage == AdvantageType.ADVANTAGE:
        return max(roll1, roll2), min(roll1, roll2)
    else:  # DISADVANTAGE
        return min(roll1, roll2), max(roll1, roll2)


def calculate_attack_roll(request: AttackRollRequest) -> AttackRollResponse:
    """
    Calculate an attack roll with advantage/disadvantage.

    Args:
        request: Attack roll parameters

    Returns:
        Attack roll result with hit determination
    """
    roll, second_roll = roll_d20_with_advantage(request.advantage)
    total = roll + request.attack_bonus

    # Natural 20 is always a crit, natural 1 is always a miss
    critical_hit = roll == 20
    critical_miss = roll == 1

    # Determine if attack hits (natural 20 always hits, natural 1 always misses)
    if critical_hit:
        hit = True
    elif critical_miss:
        hit = False
    else:
        hit = total >= request.armor_class

    return AttackRollResponse(
        roll=roll,
        second_roll=second_roll,
        attack_bonus=request.attack_bonus,
        total=total,
        armor_class=request.armor_class,
        hit=hit,
        critical_hit=critical_hit,
        critical_miss=critical_miss,
        advantage=request.advantage,
    )


def calculate_damage_roll(request: DamageRollRequest) -> DamageRollResponse:
    """
    Calculate damage with optional critical hit.

    Args:
        request: Damage roll parameters

    Returns:
        Damage roll result
    """
    num_dice, die_size, modifier = parse_dice_notation(request.damage_dice)

    # On a critical hit, double the number of dice (not the modifier)
    if request.critical_hit:
        num_dice *= 2

    # Roll each die individually to show breakdown
    rolls = [random.randint(1, die_size) for _ in range(num_dice)]
    total = sum(rolls) + modifier

    return DamageRollResponse(
        rolls=rolls,
        modifier=modifier,
        total=total,
        damage_type=request.damage_type,
        critical_hit=request.critical_hit,
    )


def calculate_saving_throw(request: SavingThrowRequest) -> SavingThrowResponse:
    """
    Calculate a saving throw with advantage/disadvantage.

    Args:
        request: Saving throw parameters

    Returns:
        Saving throw result with success determination
    """
    roll, second_roll = roll_d20_with_advantage(request.advantage)
    total = roll + request.ability_modifier + request.proficiency_bonus

    success = total >= request.dc
    natural_20 = roll == 20
    natural_1 = roll == 1

    return SavingThrowResponse(
        roll=roll,
        second_roll=second_roll,
        ability_modifier=request.ability_modifier,
        proficiency_bonus=request.proficiency_bonus,
        total=total,
        dc=request.dc,
        success=success,
        natural_20=natural_20,
        natural_1=natural_1,
        advantage=request.advantage,
    )


def calculate_full_combat(request: CombatCalculatorRequest) -> CombatCalculatorResponse:
    """
    Calculate a full combat turn (attack + damage if hit).

    Args:
        request: Full combat parameters

    Returns:
        Complete combat result with attack and optional damage
    """
    # Calculate attack roll
    attack_request = AttackRollRequest(
        attack_bonus=request.attack_bonus,
        armor_class=request.armor_class,
        advantage=request.advantage,
    )
    attack_result = calculate_attack_roll(attack_request)

    # If attack hits, calculate damage
    damage_result = None
    if attack_result.hit:
        damage_request = DamageRollRequest(
            damage_dice=request.damage_dice,
            damage_type=request.damage_type,
            critical_hit=attack_result.critical_hit,
        )
        damage_result = calculate_damage_roll(damage_request)

    return CombatCalculatorResponse(
        attack=attack_result,
        damage=damage_result,
    )
