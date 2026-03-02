"""Tests for character API endpoints"""


def test_get_characters(client):
    """Test getting all characters"""
    response = client.get("/api/v1/characters")
    assert response.status_code == 200
    data = response.json()
    assert "characters" in data
    assert "total" in data
    assert "skip" in data
    assert "limit" in data
    assert isinstance(data["characters"], list)
    assert data["skip"] == 0
    assert data["limit"] == 10


def test_get_characters_filter_by_class(client):
    """Test filtering characters by class"""
    response = client.get("/api/v1/characters?class=Wizard")
    assert response.status_code == 200
    data = response.json()
    assert "characters" in data
    assert "total" in data
    # All returned characters should be Wizards
    for char in data["characters"]:
        assert char["class"] == "Wizard"


def test_get_characters_filter_by_race(client):
    """Test filtering characters by race"""
    response = client.get("/api/v1/characters?race=Elf")
    assert response.status_code == 200
    data = response.json()
    assert "characters" in data
    for char in data["characters"]:
        assert char["race"] == "Elf"


def test_get_characters_search_by_name(client):
    """Test searching characters by name"""
    response = client.get("/api/v1/characters?name=raistlin")
    assert response.status_code == 200
    data = response.json()
    assert "characters" in data
    # Should find Raistlin Majere
    for char in data["characters"]:
        assert "raistlin" in char["name"].lower()


def test_get_character_by_id(client):
    """Test getting a specific character by ID"""
    response = client.get("/api/v1/characters/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "race" in data
    assert "class" in data


def test_get_character_by_id_not_found(client):
    """Test getting a non-existent character"""
    response = client.get("/api/v1/characters/99999")
    assert response.status_code == 404


def test_get_random_character(client):
    """Test generating a random character"""
    response = client.get("/api/v1/characters/random")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "name" in data
    assert "race" in data
    assert "class" in data
    assert "stats" in data
    assert "description" in data

    # Validate stats structure
    stats = data["stats"]
    assert all(
        key in stats
        for key in [
            "strength",
            "dexterity",
            "constitution",
            "intelligence",
            "wisdom",
            "charisma",
        ]
    )
    assert all(3 <= stats[key] <= 18 for key in stats)


def test_ravyn_character_sheet_fields(client):
    """Test that Ravyn Dusk'rel returns extended character-sheet fields"""
    response = client.get("/api/v1/characters?name=ravyn&limit=100")
    assert response.status_code == 200
    data = response.json()

    character = next(
        (c for c in data["characters"] if c["name"] == "Ravyn Dusk'rel"), None
    )
    assert character is not None
    assert character["class"] == "Ranger"
    assert character["level"] == 1
    assert character["proficiency_bonus"] == 2
    assert character["armor_class"] == 15
    assert character["hit_points"]["current"] == 13
    assert character["senses"]["darkvision"] == 120
    assert isinstance(character["skills"], list)
    stealth = next((s for s in character["skills"] if s["skill"] == "stealth"), None)
    assert stealth is not None
    assert stealth["bonus"] == 7
    assert stealth["proficient"] is True
    assert len(character["actions"]) >= 1
