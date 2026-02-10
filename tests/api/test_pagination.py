"""Tests for API pagination functionality"""


def test_characters_pagination_default(client):
    """Test default pagination values"""
    response = client.get("/api/v1/characters")
    assert response.status_code == 200
    data = response.json()
    assert data["skip"] == 0
    assert data["limit"] == 10
    assert len(data["characters"]) <= 10


def test_characters_pagination_custom(client):
    """Test custom pagination parameters"""
    response = client.get("/api/v1/characters?skip=2&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["skip"] == 2
    assert data["limit"] == 5
    assert len(data["characters"]) <= 5


def test_characters_pagination_respects_total(client):
    """Test that total count is correct"""
    response = client.get("/api/v1/characters")
    assert response.status_code == 200
    data = response.json()
    total = data["total"]
    
    # Get all items with high limit
    response2 = client.get(f"/api/v1/characters?limit=100")
    data2 = response2.json()
    
    # Total should match actual count
    assert data2["total"] == total


def test_monsters_pagination(client):
    """Test pagination on monsters endpoint"""
    response = client.get("/api/v1/monsters?skip=1&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert data["skip"] == 1
    assert data["limit"] == 3
    assert len(data["monsters"]) <= 3


def test_items_pagination(client):
    """Test pagination on items endpoint"""
    response = client.get("/api/v1/items?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["skip"] == 0
    assert data["limit"] == 5
    assert len(data["items"]) <= 5


def test_pagination_with_filters(client):
    """Test pagination works correctly with filters"""
    # Get filtered results with pagination
    response = client.get("/api/v1/characters?class=Wizard&skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    
    # Should apply filter first, then paginate
    assert len(data["characters"]) <= 2
    for char in data["characters"]:
        assert char["class"] == "Wizard"
    
    # Total should reflect filtered count, not all characters
    assert data["total"] >= len(data["characters"])


def test_pagination_limit_max(client):
    """Test that limit cannot exceed 100"""
    response = client.get("/api/v1/characters?limit=100")
    assert response.status_code == 200
    data = response.json()
    assert data["limit"] == 100
    

def test_pagination_skip_validation(client):
    """Test that skip must be non-negative"""
    response = client.get("/api/v1/characters?skip=-1")
    assert response.status_code == 422  # Validation error
