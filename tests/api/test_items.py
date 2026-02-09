"""Tests for item API endpoints"""


def test_get_items(client):
    """Test getting all items"""
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "skip" in data
    assert "limit" in data
    assert isinstance(data["items"], list)
    assert data["skip"] == 0
    assert data["limit"] == 10


def test_get_items_filter_by_type(client):
    """Test filtering items by type"""
    response = client.get("/api/v1/items?type=Weapon")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    for item in data["items"]:
        assert item["type"] == "Weapon"


def test_get_items_filter_by_rarity(client):
    """Test filtering items by rarity"""
    response = client.get("/api/v1/items?rarity=Rare")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    for item in data["items"]:
        assert item["rarity"] == "Rare"


def test_get_items_filter_by_magic(client):
    """Test filtering items by magic property"""
    response = client.get("/api/v1/items?magic=true")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    for item in data["items"]:
        assert item["magic"] is True


def test_get_items_filter_by_cost_range(client):
    """Test filtering items by cost range"""
    response = client.get("/api/v1/items?min_cost=100&max_cost=500")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    for item in data["items"]:
        assert 100 <= item["cost"] <= 500


def test_get_items_search_by_name(client):
    """Test searching items by name"""
    response = client.get("/api/v1/items?name=sword")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    for item in data["items"]:
        assert "sword" in item["name"].lower()


def test_get_item_by_id(client):
    """Test getting a specific item by ID"""
    response = client.get("/api/v1/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "type" in data
    assert "rarity" in data


def test_get_item_by_id_not_found(client):
    """Test getting a non-existent item"""
    response = client.get("/api/v1/items/99999")
    assert response.status_code == 404


def test_get_items_multiple_filters(client):
    """Test combining multiple filters"""
    response = client.get("/api/v1/items?type=Weapon&magic=true&min_cost=100")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    for item in data["items"]:
        assert item["type"] == "Weapon"
        assert item["magic"] is True
        assert item["cost"] >= 100
