"""Tests for utility functions - dice rolling"""

import pytest
from app.utils.dice import (
    roll_dice,
    roll_ability_score,
    parse_dice_notation,
    roll_from_notation,
)


def test_roll_dice_basic():
    """Test basic dice rolling"""
    result = roll_dice(2, 6)
    assert 2 <= result <= 12  # 2d6 range


def test_roll_dice_with_modifier():
    """Test dice rolling with modifier"""
    result = roll_dice(1, 20, 5)
    assert 6 <= result <= 25  # 1d20+5 range


def test_roll_ability_score():
    """Test ability score rolling (4d6 drop lowest)"""
    for _ in range(10):  # Test multiple times
        score = roll_ability_score()
        assert 3 <= score <= 18


def test_parse_dice_notation_basic():
    """Test parsing basic dice notation"""
    num, size, mod = parse_dice_notation("2d6")
    assert num == 2
    assert size == 6
    assert mod == 0


def test_parse_dice_notation_with_positive_modifier():
    """Test parsing dice notation with positive modifier"""
    num, size, mod = parse_dice_notation("3d8+5")
    assert num == 3
    assert size == 8
    assert mod == 5


def test_parse_dice_notation_with_negative_modifier():
    """Test parsing dice notation with negative modifier"""
    num, size, mod = parse_dice_notation("1d20-2")
    assert num == 1
    assert size == 20
    assert mod == -2


def test_roll_from_notation():
    """Test rolling from notation string"""
    result = roll_from_notation("1d6+2")
    assert 3 <= result <= 8  # 1d6+2 range
