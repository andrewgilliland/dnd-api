"""Test configuration and fixtures"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def sample_character():
    """Sample character data for testing"""
    return {
        "id": 1,
        "name": "Test Hero",
        "race": "Human",
        "class": "Fighter",
        "alignment": "Lawful Good",
        "description": "A brave test character",
        "stats": {
            "strength": 16,
            "dexterity": 14,
            "constitution": 15,
            "intelligence": 10,
            "wisdom": 12,
            "charisma": 13,
        },
    }


@pytest.fixture
def sample_monster():
    """Sample monster data for testing"""
    return {
        "id": 1,
        "name": "Test Dragon",
        "type": "Dragon",
        "size": "Huge",
        "alignment": "Chaotic Evil",
        "armor_class": 19,
        "hit_points": 200,
        "hit_dice": "16d12+96",
        "challenge_rating": 13.0,
        "experience_points": 10000,
    }


@pytest.fixture
def sample_party():
    """Sample party data for testing"""
    return {
        "name": "Test Party",
        "members": [
            {
                "characterId": 1,
                "role": "tank",
                "isLeader": True,
                "marchingOrder": 1,
            },
            {
                "characterId": 2,
                "role": "healer",
                "isLeader": False,
                "marchingOrder": 2,
            },
            {
                "characterId": 3,
                "role": "caster",
                "isLeader": False,
                "marchingOrder": 3,
            },
        ],
        "notes": "A test party for D&D adventures",
        "tags": ["test", "campaign"],
    }


@pytest.fixture
def sample_party_member():
    """Sample party member data for testing"""
    return {
        "characterId": 1,
        "role": "tank",
        "isLeader": True,
        "marchingOrder": 1,
    }


@pytest.fixture
def sample_item():
    """Sample item data for testing"""
    return {
        "id": 1,
        "name": "Test Sword",
        "type": "Weapon",
        "category": "Martial Melee Weapon",
        "rarity": "Rare",
        "description": "A magical test sword",
        "cost": 500,
        "weight": 3.0,
        "properties": ["Versatile"],
        "magic": True,
        "attunement_required": False,
        "damage": "1d8",
        "damage_type": "Slashing",
    }
