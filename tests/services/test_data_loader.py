"""Tests for data loader functions"""

import pytest
from app.services.data_loader import (
    load_characters,
    load_monsters,
    load_items,
    load_character_names,
    load_character_traits,
    load_monster_names,
)


def test_load_characters():
    """Test loading character data"""
    characters = load_characters()
    assert isinstance(characters, list)
    assert len(characters) > 0

    # Check first character has required fields
    char = characters[0]
    assert "id" in char
    assert "name" in char
    assert "race" in char
    assert "class" in char


def test_load_monsters():
    """Test loading monster data"""
    monsters = load_monsters()
    assert isinstance(monsters, list)
    assert len(monsters) > 0

    # Check first monster has required fields
    monster = monsters[0]
    assert "id" in monster
    assert "name" in monster
    assert "type" in monster
    assert "challenge_rating" in monster


def test_load_items():
    """Test loading item data"""
    items = load_items()
    assert isinstance(items, list)
    assert len(items) > 0

    # Check first item has required fields
    item = items[0]
    assert "id" in item
    assert "name" in item
    assert "type" in item
    assert "rarity" in item


def test_load_character_names():
    """Test loading character names data"""
    names = load_character_names()
    assert isinstance(names, dict)
    assert len(names) > 0
    assert "Human" in names
    assert isinstance(names["Human"], list)


def test_load_character_traits():
    """Test loading character traits data"""
    traits = load_character_traits()
    assert isinstance(traits, dict)
    assert "class_traits" in traits
    assert "alignment_motivations" in traits
    assert "race_backgrounds" in traits
    assert "description_templates" in traits


def test_load_monster_names():
    """Test loading monster names data"""
    names = load_monster_names()
    assert isinstance(names, dict)
    assert "prefixes" in names
    assert "suffixes" in names
    assert "Dragon" in names["prefixes"]
    assert "Dragon" in names["suffixes"]


def test_data_loader_caching():
    """Test that data loader uses caching"""
    # Call twice, should return same object due to lru_cache
    chars1 = load_characters()
    chars2 = load_characters()
    assert chars1 is chars2  # Same object reference due to caching
