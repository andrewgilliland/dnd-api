"""Tests for monster API endpoints"""


def test_get_monsters(client):
    """Test getting all monsters"""
    response = client.get("/api/v1/monsters")
    assert response.status_code == 200
    data = response.json()
    assert "monsters" in data
    assert "total" in data
    assert "skip" in data
    assert "limit" in data
    assert isinstance(data["monsters"], list)
    assert data["skip"] == 0
    assert data["limit"] == 10


def test_get_monsters_filter_by_type(client):
    """Test filtering monsters by type"""
    response = client.get("/api/v1/monsters?type=Dragon")
    assert response.status_code == 200
    data = response.json()
    assert "monsters" in data
    assert "total" in data
    for monster in data["monsters"]:
        assert monster["type"] == "Dragon"


def test_get_monsters_filter_by_size(client):
    """Test filtering monsters by size"""
    response = client.get("/api/v1/monsters?size=Large")
    assert response.status_code == 200
    data = response.json()
    assert "monsters" in data
    for monster in data["monsters"]:
        assert monster["size"] == "Large"


def test_get_monsters_filter_by_cr_range(client):
    """Test filtering monsters by challenge rating range"""
    response = client.get("/api/v1/monsters?min_cr=5&max_cr=10")
    assert response.status_code == 200
    data = response.json()
    assert "monsters" in data
    for monster in data["monsters"]:
        assert 5 <= monster["challenge_rating"] <= 10


def test_get_monsters_search_by_name(client):
    """Test searching monsters by name"""
    response = client.get("/api/v1/monsters?name=dragon")
    assert response.status_code == 200
    data = response.json()
    assert "monsters" in data
    for monster in data["monsters"]:
        assert "dragon" in monster["name"].lower()


def test_get_monster_by_id(client):
    """Test getting a specific monster by ID"""
    response = client.get("/api/v1/monsters/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "type" in data
    assert "challenge_rating" in data


def test_get_monster_by_id_not_found(client):
    """Test getting a non-existent monster"""
    response = client.get("/api/v1/monsters/99999")
    assert response.status_code == 404


def test_get_random_monster(client):
    """Test generating a random monster"""
    response = client.get("/api/v1/monsters/random")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "name" in data
    assert "type" in data
    assert "size" in data
    assert "challenge_rating" in data
    assert "actions" in data


def test_get_random_monster_with_filters(client):
    """Test generating a random monster with filters"""
    response = client.get("/api/v1/monsters/random?type=Dragon&min_cr=5&max_cr=10")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "Dragon"
    assert 5 <= data["challenge_rating"] <= 10
