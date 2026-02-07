"""Tests for character service functions"""

import pytest
from app.services.character_service import (
    generate_random_stats,
    generate_random_name,
    generate_random_description,
    generate_random_character,
)
from app.models import Race, Class, Alignment


def test_generate_random_stats():
    """Test random stats generation"""
    stats = generate_random_stats()

    # Check all stats are present
    assert hasattr(stats, "strength")
    assert hasattr(stats, "dexterity")
    assert hasattr(stats, "constitution")
    assert hasattr(stats, "intelligence")
    assert hasattr(stats, "wisdom")
    assert hasattr(stats, "charisma")

    # Check all stats are in valid range (3-18 for 4d6 drop lowest)
    assert 3 <= stats.strength <= 18
    assert 3 <= stats.dexterity <= 18
    assert 3 <= stats.constitution <= 18
    assert 3 <= stats.intelligence <= 18
    assert 3 <= stats.wisdom <= 18
    assert 3 <= stats.charisma <= 18


def test_generate_random_name():
    """Test random name generation"""
    name = generate_random_name(Race.HUMAN, Class.FIGHTER)
    assert isinstance(name, str)
    assert len(name) > 0


def test_generate_random_description():
    """Test random description generation"""
    description = generate_random_description(
        "Test Hero", Race.HUMAN, Class.FIGHTER, Alignment.LAWFUL_GOOD
    )
    assert isinstance(description, str)
    assert len(description) > 0
    assert "Test Hero" in description


def test_generate_random_character():
    """Test full random character generation"""
    character = generate_random_character()

    assert character.id > 0
    assert len(character.name) > 0
    assert character.race in Race
    assert character.class_ in Class
    assert character.alignment in Alignment
    assert len(character.description) > 0
    assert character.stats is not None
