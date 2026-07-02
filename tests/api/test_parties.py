"""Tests for party API endpoints"""

from datetime import datetime


def test_get_parties(client):
    """Test getting all parties"""
    response = client.get("/api/v1/parties")
    assert response.status_code == 200
    data = response.json()
    assert "parties" in data
    assert "total" in data
    assert "skip" in data
    assert "limit" in data
    assert isinstance(data["parties"], list)
    assert data["skip"] == 0
    assert data["limit"] == 10
    assert data["total"] >= 2  # At least the 2 mock parties


def test_get_parties_pagination(client):
    """Test party pagination"""
    # Skip first party
    response = client.get("/api/v1/parties?skip=1&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["parties"]) <= 1
    assert data["skip"] == 1
    assert data["limit"] == 1


def test_get_parties_filter_by_name(client):
    """Test filtering parties by name"""
    response = client.get("/api/v1/parties?name=stormbreakers")
    assert response.status_code == 200
    data = response.json()
    assert len(data["parties"]) == 1
    assert data["parties"][0]["name"] == "Stormbreakers"


def test_get_parties_filter_by_name_partial(client):
    """Test partial name filtering"""
    response = client.get("/api/v1/parties?name=shadow")
    assert response.status_code == 200
    data = response.json()
    assert len(data["parties"]) == 1
    assert "Shadow" in data["parties"][0]["name"]


def test_get_parties_filter_no_results(client):
    """Test filtering with no matching results"""
    response = client.get("/api/v1/parties?name=nonexistent")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert len(data["parties"]) == 0


def test_get_parties_returns_camelcase(client):
    """Test that response uses camelCase for field names"""
    response = client.get("/api/v1/parties")
    assert response.status_code == 200
    data = response.json()
    party = data["parties"][0]
    
    # Check camelCase field names
    assert "createdByUserId" in party
    assert "createdAt" in party
    assert "updatedAt" in party
    assert "isLeader" in party["members"][0]
    assert "characterId" in party["members"][0]
    assert "marchingOrder" in party["members"][0]
    assert "joinedAt" in party["members"][0]


def test_create_party(client):
    """Test creating a new party"""
    party_data = {
        "name": "Test Party",
        "members": [
            {
                "characterId": 10,
                "role": "tank",
                "isLeader": True,
                "marchingOrder": 1,
            },
            {
                "characterId": 11,
                "role": "healer",
                "isLeader": False,
                "marchingOrder": 2,
            },
        ],
        "notes": "A test party",
        "tags": ["test"],
    }
    
    response = client.post("/api/v1/parties", json=party_data)
    assert response.status_code == 200
    data = response.json()
    
    # Check structure
    assert data["id"]
    assert data["name"] == "Test Party"
    assert data["status"] == "active"
    assert len(data["members"]) == 2
    assert data["notes"] == "A test party"
    assert data["tags"] == ["test"]
    
    # Check timestamps were set
    assert data["createdAt"]
    assert data["updatedAt"]
    assert data["createdByUserId"] == "current-user"


def test_create_party_minimal(client):
    """Test creating a party with minimal data"""
    party_data = {
        "name": "Minimal Party",
        "members": [
            {
                "characterId": 20,
                "role": "scout",
                "isLeader": True,
                "marchingOrder": 1,
            },
        ],
    }
    
    response = client.post("/api/v1/parties", json=party_data)
    assert response.status_code == 200
    data = response.json()
    
    assert data["name"] == "Minimal Party"
    assert len(data["members"]) == 1
    assert data["notes"] is None or data["notes"] == ""
    assert data["tags"] is None or data["tags"] == []


def test_create_party_member_structure(client):
    """Test that created party members have proper structure"""
    party_data = {
        "name": "Member Test Party",
        "members": [
            {
                "characterId": 30,
                "role": "caster",
                "isLeader": False,
                "marchingOrder": 1,
            },
        ],
    }
    
    response = client.post("/api/v1/parties", json=party_data)
    assert response.status_code == 200
    data = response.json()
    
    member = data["members"][0]
    # Check camelCase field names
    assert member["characterId"] == 30
    assert member["role"] == "caster"
    assert member["isLeader"] is False
    assert member["marchingOrder"] == 1
    assert member["joinedAt"]  # Should have auto-set timestamp


def test_created_party_is_retrievable(client):
    """Test that created parties appear in get_parties"""
    # Create a party
    party_data = {
        "name": "Retrievable Party",
        "members": [
            {
                "characterId": 40,
                "role": "tank",
                "isLeader": True,
                "marchingOrder": 1,
            },
        ],
    }
    
    create_response = client.post("/api/v1/parties", json=party_data)
    assert create_response.status_code == 200
    created_id = create_response.json()["id"]
    
    # Retrieve all parties and find the created one
    get_response = client.get("/api/v1/parties")
    assert get_response.status_code == 200
    parties = get_response.json()["parties"]
    
    created_party = next((p for p in parties if p["id"] == created_id), None)
    assert created_party is not None
    assert created_party["name"] == "Retrievable Party"


def test_create_party_with_all_roles(client):
    """Test creating party with various valid roles"""
    party_data = {
        "name": "All Roles Party",
        "members": [
            {"characterId": 50, "role": "tank", "isLeader": True, "marchingOrder": 1},
            {"characterId": 51, "role": "support", "isLeader": False, "marchingOrder": 2},
            {"characterId": 52, "role": "healer", "isLeader": False, "marchingOrder": 3},
            {"characterId": 53, "role": "scout", "isLeader": False, "marchingOrder": 4},
            {"characterId": 54, "role": "face", "isLeader": False, "marchingOrder": 5},
            {"characterId": 55, "role": "caster", "isLeader": False, "marchingOrder": 6},
            {"characterId": 56, "role": "striker", "isLeader": False, "marchingOrder": 7},
            {"characterId": 57, "role": "controller", "isLeader": False, "marchingOrder": 8},
        ],
    }
    
    response = client.post("/api/v1/parties", json=party_data)
    assert response.status_code == 200
    data = response.json()
    assert len(data["members"]) == 8
    assert data["members"][0]["role"] == "tank"
    assert data["members"][7]["role"] == "controller"
