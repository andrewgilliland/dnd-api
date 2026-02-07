"""Tests for monster service functions"""

import pytest
from app.services.monster_service import (
    generate_random_monster_name,
    generate_random_monster_stats,
    generate_special_abilities,
    generate_monster_actions,
    generate_random_monster,
)
from app.models import MonsterType, Size


def test_generate_random_monster_name():
    """Test random monster name generation"""
    name = generate_random_monster_name(MonsterType.DRAGON)
    assert isinstance(name, str)
    assert len(name) > 0


def test_generate_random_monster_stats():
    """Test random monster stats generation"""
    stats = generate_random_monster_stats(5.0)

    assert hasattr(stats, "strength")
    assert hasattr(stats, "dexterity")
    assert hasattr(stats, "constitution")
    assert hasattr(stats, "intelligence")
    assert hasattr(stats, "wisdom")
    assert hasattr(stats, "charisma")

    # Stats should be reasonable for CR 5
    assert all(
        stat > 0
        for stat in [
            stats.strength,
            stats.dexterity,
            stats.constitution,
            stats.intelligence,
            stats.wisdom,
            stats.charisma,
        ]
    )


def test_generate_special_abilities():
    """Test special abilities generation"""
    abilities = generate_special_abilities(MonsterType.DRAGON, 10.0)

    if abilities:  # Some types may have abilities
        assert isinstance(abilities, list)
        for ability in abilities:
            assert hasattr(ability, "name")
            assert hasattr(ability, "description")


def test_generate_monster_actions():
    """Test monster actions generation"""
    actions = generate_monster_actions(MonsterType.DRAGON, 10.0)

    assert isinstance(actions, list)
    assert len(actions) > 0

    for action in actions:
        assert hasattr(action, "name")
        assert hasattr(action, "description")


def test_generate_random_monster():
    """Test full random monster generation"""
    monster = generate_random_monster()

    assert monster.id > 0
    assert len(monster.name) > 0
    assert monster.type in MonsterType
    assert monster.size in Size
    assert monster.challenge_rating >= 0
    assert monster.hit_points > 0
    assert monster.armor_class > 0
    assert len(monster.actions) > 0


def test_generate_random_monster_with_filters():
    """Test random monster generation with filters"""
    monster = generate_random_monster(
        monster_type=MonsterType.DRAGON, size=Size.HUGE, min_cr=5.0, max_cr=10.0
    )

    assert monster.type == MonsterType.DRAGON
    assert monster.size == Size.HUGE
    assert 5.0 <= monster.challenge_rating <= 10.0
