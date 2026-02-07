"""Tests for utility functions - calculations"""

import pytest
from app.utils.calculations import (
    calculate_modifier,
    calculate_proficiency_bonus,
    calculate_hp_from_cr,
    calculate_ac_from_cr,
    get_xp_by_cr,
)
from app.models import Size


def test_calculate_modifier():
    """Test ability modifier calculation"""
    assert calculate_modifier(10) == 0
    assert calculate_modifier(11) == 0
    assert calculate_modifier(12) == 1
    assert calculate_modifier(16) == 3
    assert calculate_modifier(20) == 5
    assert calculate_modifier(8) == -1
    assert calculate_modifier(1) == -5


def test_calculate_proficiency_bonus():
    """Test proficiency bonus calculation"""
    assert calculate_proficiency_bonus(1) == 2
    assert calculate_proficiency_bonus(5) == 3
    assert calculate_proficiency_bonus(9) == 4
    assert calculate_proficiency_bonus(13) == 5
    assert calculate_proficiency_bonus(17) == 6
    assert calculate_proficiency_bonus(20) == 6


def test_calculate_hp_from_cr():
    """Test HP calculation from CR and size"""
    hp, dice = calculate_hp_from_cr(5.0, Size.LARGE)
    assert hp > 0
    assert "d10" in dice  # Large creatures use d10
    assert isinstance(hp, int)
    assert isinstance(dice, str)


def test_calculate_ac_from_cr():
    """Test AC calculation from CR"""
    ac = calculate_ac_from_cr(1.0)
    assert 10 <= ac <= 25

    ac_high = calculate_ac_from_cr(20.0)
    assert ac_high >= ac  # Higher CR should have higher AC


def test_get_xp_by_cr():
    """Test XP lookup by CR"""
    assert get_xp_by_cr(0) == 10
    assert get_xp_by_cr(1) == 200
    assert get_xp_by_cr(5) == 1800
    assert get_xp_by_cr(10) == 5900
    assert get_xp_by_cr(20) == 25000


def test_get_xp_by_cr_invalid():
    """Test XP lookup with invalid CR"""
    assert get_xp_by_cr(999) == 0  # Should return 0 for invalid CR
