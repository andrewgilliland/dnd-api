"""Tests for spell API endpoints"""


def test_get_spells(client):
    """Test getting all spells returns expected structure"""
    response = client.get("/api/v1/spells")
    assert response.status_code == 200
    data = response.json()
    assert "spells" in data
    assert "total" in data
    assert "skip" in data
    assert "limit" in data
    assert isinstance(data["spells"], list)
    assert data["skip"] == 0
    assert data["limit"] == 10
    assert data["total"] > 0


def test_get_spells_contains_expected_fields(client):
    """Test that each spell has the required fields"""
    response = client.get("/api/v1/spells")
    assert response.status_code == 200
    spells = response.json()["spells"]
    assert len(spells) > 0
    for spell in spells:
        assert "id" in spell
        assert "name" in spell
        assert "level" in spell
        assert "school" in spell
        assert "casting_time" in spell
        assert "range" in spell
        assert "components" in spell
        assert "duration" in spell
        assert "concentration" in spell
        assert "ritual" in spell
        assert "description" in spell
        assert "classes" in spell


def test_get_spells_filter_by_school(client):
    """Test filtering spells by school of magic"""
    response = client.get("/api/v1/spells?school=Evocation&limit=100")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    for spell in data["spells"]:
        assert spell["school"] == "Evocation"


def test_get_spells_filter_by_name(client):
    """Test searching spells by name (partial, case-insensitive)"""
    response = client.get("/api/v1/spells?name=fire&limit=100")
    assert response.status_code == 200
    data = response.json()
    for spell in data["spells"]:
        assert "fire" in spell["name"].lower()


def test_get_spells_filter_by_min_level(client):
    """Test filtering spells by minimum level"""
    response = client.get("/api/v1/spells?min_level=5&limit=100")
    assert response.status_code == 200
    data = response.json()
    for spell in data["spells"]:
        assert spell["level"] >= 5


def test_get_spells_filter_by_max_level(client):
    """Test filtering spells by maximum level"""
    response = client.get("/api/v1/spells?max_level=2&limit=100")
    assert response.status_code == 200
    data = response.json()
    for spell in data["spells"]:
        assert spell["level"] <= 2


def test_get_spells_filter_by_level_range(client):
    """Test filtering spells by level range"""
    response = client.get("/api/v1/spells?min_level=3&max_level=5&limit=100")
    assert response.status_code == 200
    data = response.json()
    for spell in data["spells"]:
        assert 3 <= spell["level"] <= 5


def test_get_spells_filter_cantrips(client):
    """Test filtering for cantrips (level 0)"""
    response = client.get("/api/v1/spells?min_level=0&max_level=0&limit=100")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    for spell in data["spells"]:
        assert spell["level"] == 0


def test_get_spells_filter_by_spell_class(client):
    """Test filtering spells by class"""
    response = client.get("/api/v1/spells?spell_class=Wizard&limit=100")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    for spell in data["spells"]:
        assert any("wizard" == c.lower() for c in spell["classes"])


def test_get_spells_filter_by_concentration(client):
    """Test filtering spells by concentration requirement"""
    response = client.get("/api/v1/spells?concentration=true&limit=100")
    assert response.status_code == 200
    data = response.json()
    for spell in data["spells"]:
        assert spell["concentration"] is True


def test_get_spells_filter_no_concentration(client):
    """Test filtering spells that don't require concentration"""
    response = client.get("/api/v1/spells?concentration=false&limit=100")
    assert response.status_code == 200
    data = response.json()
    for spell in data["spells"]:
        assert spell["concentration"] is False


def test_get_spells_filter_by_ritual(client):
    """Test filtering spells by ritual casting"""
    response = client.get("/api/v1/spells?ritual=true&limit=100")
    assert response.status_code == 200
    data = response.json()
    for spell in data["spells"]:
        assert spell["ritual"] is True


def test_get_spells_pagination_skip(client):
    """Test spell pagination with skip"""
    first = client.get("/api/v1/spells?skip=0&limit=5").json()
    second = client.get("/api/v1/spells?skip=5&limit=5").json()

    assert first["skip"] == 0
    assert second["skip"] == 5

    first_ids = [s["id"] for s in first["spells"]]
    second_ids = [s["id"] for s in second["spells"]]
    assert not set(first_ids) & set(second_ids)


def test_get_spells_pagination_total_consistent(client):
    """Test that total count is consistent across pages"""
    page1 = client.get("/api/v1/spells?skip=0&limit=5").json()
    page2 = client.get("/api/v1/spells?skip=5&limit=5").json()
    assert page1["total"] == page2["total"]


def test_get_spell_by_id(client):
    """Test getting a specific spell by ID"""
    response = client.get("/api/v1/spells/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "school" in data
    assert "level" in data


def test_get_spell_by_id_not_found(client):
    """Test getting a non-existent spell returns 404"""
    response = client.get("/api/v1/spells/99999")
    assert response.status_code == 404


def test_get_random_spell(client):
    """Test generating a random spell"""
    response = client.get("/api/v1/spells/random")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "name" in data
    assert "school" in data
    assert "level" in data
    assert "classes" in data
    assert isinstance(data["classes"], list)


def test_get_random_spell_with_school(client):
    """Test generating a random spell with a school filter"""
    response = client.get("/api/v1/spells/random?school=Necromancy")
    assert response.status_code == 200
    data = response.json()
    assert data["school"] == "Necromancy"


def test_get_random_spell_with_level_range(client):
    """Test generating a random spell within a level range"""
    response = client.get("/api/v1/spells/random?min_level=3&max_level=5")
    assert response.status_code == 200
    data = response.json()
    assert 3 <= data["level"] <= 5


def test_get_random_spell_with_spell_class(client):
    """Test generating a random spell for a specific class"""
    response = client.get("/api/v1/spells/random?spell_class=Druid")
    assert response.status_code == 200
    data = response.json()
    assert "Druid" in data["classes"]


def test_get_random_spell_cantrip(client):
    """Test generating a random cantrip (level 0)"""
    response = client.get("/api/v1/spells/random?min_level=0&max_level=0")
    assert response.status_code == 200
    data = response.json()
    assert data["level"] == 0
