"""Tests for combat API endpoints"""

from unittest.mock import patch


class TestCombatCalculatorInfo:
    """Tests for combat calculator info endpoint"""

    def test_get_combat_info(self, client):
        """Test getting combat calculator information"""
        response = client.get("/api/v1/combat")
        assert response.status_code == 200
        data = response.json()
        assert "description" in data
        assert "endpoints" in data
        assert "features" in data


class TestAttackRollEndpoint:
    """Tests for attack roll endpoint"""

    def test_basic_attack_roll(self, client):
        """Test basic attack roll endpoint"""
        with patch("random.randint", return_value=15):
            response = client.post(
                "/api/v1/combat/attack-roll",
                json={"attack_bonus": 5, "armor_class": 15, "advantage": "normal"},
            )
            assert response.status_code == 200
            data = response.json()

            assert data["roll"] == 15
            assert data["attack_bonus"] == 5
            assert data["total"] == 20
            assert data["armor_class"] == 15
            assert data["hit"] is True
            assert data["critical_hit"] is False
            assert data["critical_miss"] is False
            assert data["advantage"] == "normal"
            assert data["second_roll"] is None

    def test_attack_roll_with_advantage(self, client):
        """Test attack roll with advantage"""
        with patch("random.randint", side_effect=[10, 18]):
            response = client.post(
                "/api/v1/combat/attack-roll",
                json={"attack_bonus": 3, "armor_class": 15, "advantage": "advantage"},
            )
            assert response.status_code == 200
            data = response.json()

            assert data["roll"] == 18  # Takes higher roll
            assert data["second_roll"] == 10
            assert data["total"] == 21
            assert data["hit"] is True
            assert data["advantage"] == "advantage"

    def test_attack_roll_with_disadvantage(self, client):
        """Test attack roll with disadvantage"""
        with patch("random.randint", side_effect=[18, 10]):
            response = client.post(
                "/api/v1/combat/attack-roll",
                json={
                    "attack_bonus": 3,
                    "armor_class": 15,
                    "advantage": "disadvantage",
                },
            )
            assert response.status_code == 200
            data = response.json()

            assert data["roll"] == 10  # Takes lower roll
            assert data["second_roll"] == 18
            assert data["total"] == 13
            assert data["hit"] is False
            assert data["advantage"] == "disadvantage"

    def test_critical_hit(self, client):
        """Test natural 20 (critical hit)"""
        with patch("random.randint", return_value=20):
            response = client.post(
                "/api/v1/combat/attack-roll",
                json={"attack_bonus": 0, "armor_class": 25, "advantage": "normal"},
            )
            assert response.status_code == 200
            data = response.json()

            assert data["roll"] == 20
            assert data["critical_hit"] is True
            assert data["hit"] is True  # Always hits

    def test_critical_miss(self, client):
        """Test natural 1 (critical miss)"""
        with patch("random.randint", return_value=1):
            response = client.post(
                "/api/v1/combat/attack-roll",
                json={"attack_bonus": 50, "armor_class": 10, "advantage": "normal"},
            )
            assert response.status_code == 200
            data = response.json()

            assert data["roll"] == 1
            assert data["critical_miss"] is True
            assert data["hit"] is False  # Always misses

    def test_missing_required_fields(self, client):
        """Test validation error for missing required fields"""
        response = client.post(
            "/api/v1/combat/attack-roll",
            json={
                "attack_bonus": 5
                # Missing armor_class
            },
        )
        assert response.status_code == 422  # Validation error


class TestDamageRollEndpoint:
    """Tests for damage roll endpoint"""

    def test_basic_damage_roll(self, client):
        """Test basic damage roll endpoint"""
        with patch("random.randint", side_effect=[4, 6]):
            response = client.post(
                "/api/v1/combat/damage-roll",
                json={
                    "damage_dice": "2d6+3",
                    "damage_type": "slashing",
                    "critical_hit": False,
                },
            )
            assert response.status_code == 200
            data = response.json()

            assert data["rolls"] == [4, 6]
            assert data["modifier"] == 3
            assert data["total"] == 13
            assert data["damage_type"] == "slashing"
            assert data["critical_hit"] is False

    def test_critical_damage_roll(self, client):
        """Test damage roll with critical hit"""
        with patch("random.randint", side_effect=[3, 5, 4, 6]):
            response = client.post(
                "/api/v1/combat/damage-roll",
                json={
                    "damage_dice": "2d6+3",
                    "damage_type": "piercing",
                    "critical_hit": True,
                },
            )
            assert response.status_code == 200
            data = response.json()

            assert len(data["rolls"]) == 4  # Doubled dice
            assert data["rolls"] == [3, 5, 4, 6]
            assert data["modifier"] == 3  # Not doubled
            assert data["total"] == 21
            assert data["critical_hit"] is True

    def test_damage_no_modifier(self, client):
        """Test damage roll without modifier"""
        with patch("random.randint", side_effect=[3, 4, 5]):
            response = client.post(
                "/api/v1/combat/damage-roll",
                json={
                    "damage_dice": "3d6",
                    "damage_type": "fire",
                    "critical_hit": False,
                },
            )
            assert response.status_code == 200
            data = response.json()

            assert data["rolls"] == [3, 4, 5]
            assert data["modifier"] == 0
            assert data["total"] == 12

    def test_damage_negative_modifier(self, client):
        """Test damage roll with negative modifier"""
        with patch("random.randint", return_value=5):
            response = client.post(
                "/api/v1/combat/damage-roll",
                json={
                    "damage_dice": "1d8-2",
                    "damage_type": "bludgeoning",
                    "critical_hit": False,
                },
            )
            assert response.status_code == 200
            data = response.json()

            assert data["rolls"] == [5]
            assert data["modifier"] == -2
            assert data["total"] == 3

    def test_various_damage_types(self, client):
        """Test different damage types"""
        damage_types = [
            "fire",
            "cold",
            "lightning",
            "thunder",
            "acid",
            "poison",
            "necrotic",
            "radiant",
            "force",
            "psychic",
            "slashing",
            "piercing",
            "bludgeoning",
        ]

        for dmg_type in damage_types:
            with patch("random.randint", return_value=4):
                response = client.post(
                    "/api/v1/combat/damage-roll",
                    json={
                        "damage_dice": "1d8",
                        "damage_type": dmg_type,
                        "critical_hit": False,
                    },
                )
                assert response.status_code == 200
                data = response.json()
                assert data["damage_type"] == dmg_type

    def test_invalid_damage_type(self, client):
        """Test invalid damage type returns validation error"""
        response = client.post(
            "/api/v1/combat/damage-roll",
            json={
                "damage_dice": "1d8",
                "damage_type": "invalid_type",
                "critical_hit": False,
            },
        )
        assert response.status_code == 422


class TestSavingThrowEndpoint:
    """Tests for saving throw endpoint"""

    def test_successful_save(self, client):
        """Test successful saving throw"""
        with patch("random.randint", return_value=15):
            response = client.post(
                "/api/v1/combat/saving-throw",
                json={
                    "ability_modifier": 2,
                    "proficiency_bonus": 3,
                    "dc": 15,
                    "advantage": "normal",
                },
            )
            assert response.status_code == 200
            data = response.json()

            assert data["roll"] == 15
            assert data["ability_modifier"] == 2
            assert data["proficiency_bonus"] == 3
            assert data["total"] == 20
            assert data["dc"] == 15
            assert data["success"] is True
            assert data["natural_20"] is False
            assert data["natural_1"] is False

    def test_failed_save(self, client):
        """Test failed saving throw"""
        with patch("random.randint", return_value=8):
            response = client.post(
                "/api/v1/combat/saving-throw",
                json={
                    "ability_modifier": 1,
                    "proficiency_bonus": 2,
                    "dc": 15,
                    "advantage": "normal",
                },
            )
            assert response.status_code == 200
            data = response.json()

            assert data["roll"] == 8
            assert data["total"] == 11
            assert data["success"] is False

    def test_save_with_advantage(self, client):
        """Test saving throw with advantage"""
        with patch("random.randint", side_effect=[8, 16]):
            response = client.post(
                "/api/v1/combat/saving-throw",
                json={
                    "ability_modifier": 2,
                    "proficiency_bonus": 2,
                    "dc": 15,
                    "advantage": "advantage",
                },
            )
            assert response.status_code == 200
            data = response.json()

            assert data["roll"] == 16  # Higher roll
            assert data["second_roll"] == 8
            assert data["total"] == 20
            assert data["success"] is True

    def test_natural_20_save(self, client):
        """Test natural 20 on saving throw"""
        with patch("random.randint", return_value=20):
            response = client.post(
                "/api/v1/combat/saving-throw",
                json={
                    "ability_modifier": 0,
                    "proficiency_bonus": 0,
                    "dc": 15,
                    "advantage": "normal",
                },
            )
            assert response.status_code == 200
            data = response.json()

            assert data["roll"] == 20
            assert data["natural_20"] is True
            assert data["total"] == 20
            assert data["success"] is True  # Succeeds because total >= DC

    def test_natural_1_save(self, client):
        """Test natural 1 on saving throw"""
        with patch("random.randint", return_value=1):
            response = client.post(
                "/api/v1/combat/saving-throw",
                json={
                    "ability_modifier": 0,
                    "proficiency_bonus": 0,
                    "dc": 15,
                    "advantage": "normal",
                },
            )
            assert response.status_code == 200
            data = response.json()

            assert data["roll"] == 1
            assert data["natural_1"] is True
            assert data["total"] == 1
            assert data["success"] is False  # Fails because total < DC

    def test_no_proficiency_bonus(self, client):
        """Test save without proficiency bonus"""
        with patch("random.randint", return_value=10):
            response = client.post(
                "/api/v1/combat/saving-throw",
                json={
                    "ability_modifier": 3,
                    "proficiency_bonus": 0,
                    "dc": 12,
                    "advantage": "normal",
                },
            )
            assert response.status_code == 200
            data = response.json()

            assert data["proficiency_bonus"] == 0
            assert data["total"] == 13


class TestFullCombatEndpoint:
    """Tests for full combat calculation endpoint"""

    def test_successful_combat(self, client):
        """Test full combat calculation with hit"""
        with patch("random.randint", side_effect=[15, 4, 6]):
            # 15 for attack, [4, 6] for 2d6 damage
            response = client.post(
                "/api/v1/combat/combat",
                json={
                    "attack_bonus": 5,
                    "armor_class": 15,
                    "damage_dice": "2d6+3",
                    "damage_type": "slashing",
                    "advantage": "normal",
                },
            )
            assert response.status_code == 200
            data = response.json()

            # Check attack
            assert "attack" in data
            assert data["attack"]["roll"] == 15
            assert data["attack"]["total"] == 20
            assert data["attack"]["hit"] is True

            # Check damage
            assert "damage" in data
            assert data["damage"] is not None
            assert data["damage"]["rolls"] == [4, 6]
            assert data["damage"]["total"] == 13
            assert data["damage"]["damage_type"] == "slashing"

    def test_missed_combat(self, client):
        """Test full combat calculation with miss"""
        with patch("random.randint", return_value=5):
            response = client.post(
                "/api/v1/combat/combat",
                json={
                    "attack_bonus": 2,
                    "armor_class": 15,
                    "damage_dice": "2d6+3",
                    "damage_type": "piercing",
                    "advantage": "normal",
                },
            )
            assert response.status_code == 200
            data = response.json()

            # Check attack missed
            assert data["attack"]["hit"] is False

            # No damage on miss
            assert data["damage"] is None

    def test_critical_hit_combat(self, client):
        """Test full combat with critical hit"""
        with patch("random.randint", side_effect=[20, 3, 5, 4, 6]):
            # 20 for crit, [3, 5, 4, 6] for doubled 2d6
            response = client.post(
                "/api/v1/combat/combat",
                json={
                    "attack_bonus": 5,
                    "armor_class": 15,
                    "damage_dice": "2d6+3",
                    "damage_type": "slashing",
                    "advantage": "normal",
                },
            )
            assert response.status_code == 200
            data = response.json()

            # Check critical hit
            assert data["attack"]["critical_hit"] is True
            assert data["attack"]["hit"] is True

            # Check doubled damage dice
            assert data["damage"] is not None
            assert len(data["damage"]["rolls"]) == 4
            assert data["damage"]["critical_hit"] is True
            assert data["damage"]["total"] == 21

    def test_critical_miss_combat(self, client):
        """Test full combat with critical miss"""
        with patch("random.randint", return_value=1):
            response = client.post(
                "/api/v1/combat/combat",
                json={
                    "attack_bonus": 10,
                    "armor_class": 10,
                    "damage_dice": "2d6+3",
                    "damage_type": "bludgeoning",
                    "advantage": "normal",
                },
            )
            assert response.status_code == 200
            data = response.json()

            assert data["attack"]["critical_miss"] is True
            assert data["attack"]["hit"] is False
            assert data["damage"] is None

    def test_combat_with_advantage(self, client):
        """Test full combat with advantage"""
        with patch("random.randint", side_effect=[10, 18, 5, 3]):
            # [10, 18] for advantage, [5, 3] for damage
            response = client.post(
                "/api/v1/combat/combat",
                json={
                    "attack_bonus": 3,
                    "armor_class": 15,
                    "damage_dice": "2d6+2",
                    "damage_type": "piercing",
                    "advantage": "advantage",
                },
            )
            assert response.status_code == 200
            data = response.json()

            assert data["attack"]["roll"] == 18
            assert data["attack"]["second_roll"] == 10
            assert data["attack"]["hit"] is True
            assert data["damage"]["total"] == 10

    def test_combat_with_disadvantage(self, client):
        """Test full combat with disadvantage"""
        with patch("random.randint", side_effect=[18, 10]):
            response = client.post(
                "/api/v1/combat/combat",
                json={
                    "attack_bonus": 3,
                    "armor_class": 15,
                    "damage_dice": "2d6+2",
                    "damage_type": "slashing",
                    "advantage": "disadvantage",
                },
            )
            assert response.status_code == 200
            data = response.json()

            assert data["attack"]["roll"] == 10  # Lower roll
            assert data["attack"]["second_roll"] == 18
            assert data["attack"]["hit"] is False
            assert data["damage"] is None
