"""Tests for utility functions - validators"""

import pytest
from app.utils.validators import (
    validate_ability_score,
    validate_level,
    validate_challenge_rating,
    validate_dice_notation,
)


def test_validate_ability_score_valid():
    """Test validation of valid ability scores"""
    assert validate_ability_score(1) is True
    assert validate_ability_score(10) is True
    assert validate_ability_score(18) is True
    assert validate_ability_score(30) is True


def test_validate_ability_score_invalid():
    """Test validation of invalid ability scores"""
    assert validate_ability_score(0) is False
    assert validate_ability_score(-5) is False
    assert validate_ability_score(31) is False
    assert validate_ability_score(100) is False


def test_validate_level_valid():
    """Test validation of valid character levels"""
    assert validate_level(1) is True
    assert validate_level(10) is True
    assert validate_level(20) is True


def test_validate_level_invalid():
    """Test validation of invalid character levels"""
    assert validate_level(0) is False
    assert validate_level(-1) is False
    assert validate_level(21) is False
    assert validate_level(100) is False


def test_validate_challenge_rating_valid():
    """Test validation of valid challenge ratings"""
    assert validate_challenge_rating(0) is True
    assert validate_challenge_rating(0.125) is True
    assert validate_challenge_rating(0.25) is True
    assert validate_challenge_rating(0.5) is True
    assert validate_challenge_rating(1) is True
    assert validate_challenge_rating(10) is True
    assert validate_challenge_rating(30) is True


def test_validate_challenge_rating_invalid():
    """Test validation of invalid challenge ratings"""
    assert validate_challenge_rating(-1) is False
    assert validate_challenge_rating(0.3) is False  # Not a valid CR
    assert validate_challenge_rating(31) is False
    assert validate_challenge_rating(100) is False


def test_validate_dice_notation_valid():
    """Test validation of valid dice notation"""
    assert validate_dice_notation("1d6") is True
    assert validate_dice_notation("2d8") is True
    assert validate_dice_notation("3d10+5") is True
    assert validate_dice_notation("1d20-2") is True
    assert validate_dice_notation("10d12+20") is True


def test_validate_dice_notation_invalid():
    """Test validation of invalid dice notation"""
    assert validate_dice_notation("d6") is False
    assert validate_dice_notation("2d") is False
    assert validate_dice_notation("abc") is False
    assert validate_dice_notation("2d6+") is False
    assert validate_dice_notation("2d6++5") is False
