"""Tests for game data API endpoints"""

import pytest


def test_get_classes(client):
    """Test getting all character classes"""
    response = client.get("/api/v1/classes")
    assert response.status_code == 200
    data = response.json()
    assert "classes" in data
    assert isinstance(data["classes"], list)
    assert len(data["classes"]) == 12  # 12 D&D classes
    assert "Wizard" in data["classes"]
    assert "Fighter" in data["classes"]


def test_get_races(client):
    """Test getting all character races"""
    response = client.get("/api/v1/races")
    assert response.status_code == 200
    data = response.json()
    assert "races" in data
    assert isinstance(data["races"], list)
    assert len(data["races"]) == 9  # 9 D&D races
    assert "Human" in data["races"]
    assert "Elf" in data["races"]
