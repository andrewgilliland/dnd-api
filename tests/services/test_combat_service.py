"""Tests for combat service functions"""

from unittest.mock import patch
from app.services.combat_service import (
    roll_d20_with_advantage,
    calculate_attack_roll,
    calculate_damage_roll,
    calculate_saving_throw,
    calculate_full_combat,
)
from app.models.combat import (
    AdvantageType,
    AttackRollRequest,
    DamageRollRequest,
    SavingThrowRequest,
    CombatCalculatorRequest,
    DamageType,
)


class TestRollD20WithAdvantage:
    """Tests for d20 roll with advantage/disadvantage"""

    def test_normal_roll_returns_single_value(self):
        """Test normal roll returns one value and None for second roll"""
        roll, second_roll = roll_d20_with_advantage(AdvantageType.NORMAL)
        assert 1 <= roll <= 20
        assert second_roll is None

    def test_advantage_returns_higher_value(self):
        """Test advantage returns the higher of two rolls"""
        with patch("random.randint", side_effect=[5, 15]):
            roll, second_roll = roll_d20_with_advantage(AdvantageType.ADVANTAGE)
            assert roll == 15  # Higher value
            assert second_roll == 5  # Lower value

    def test_disadvantage_returns_lower_value(self):
        """Test disadvantage returns the lower of two rolls"""
        with patch("random.randint", side_effect=[15, 5]):
            roll, second_roll = roll_d20_with_advantage(AdvantageType.DISADVANTAGE)
            assert roll == 5  # Lower value
            assert second_roll == 15  # Higher value


class TestCalculateAttackRoll:
    """Tests for attack roll calculations"""

    def test_basic_attack_hit(self):
        """Test basic attack that hits"""
        with patch("random.randint", return_value=15):
            request = AttackRollRequest(
                attack_bonus=5, armor_class=15, advantage=AdvantageType.NORMAL
            )
            result = calculate_attack_roll(request)

            assert result.roll == 15
            assert result.second_roll is None
            assert result.attack_bonus == 5
            assert result.total == 20  # 15 + 5
            assert result.armor_class == 15
            assert result.hit is True
            assert result.critical_hit is False
            assert result.critical_miss is False

    def test_basic_attack_miss(self):
        """Test basic attack that misses"""
        with patch("random.randint", return_value=5):
            request = AttackRollRequest(
                attack_bonus=2, armor_class=15, advantage=AdvantageType.NORMAL
            )
            result = calculate_attack_roll(request)

            assert result.roll == 5
            assert result.total == 7  # 5 + 2
            assert result.hit is False

    def test_critical_hit_natural_20(self):
        """Test natural 20 is always a critical hit"""
        with patch("random.randint", return_value=20):
            request = AttackRollRequest(
                attack_bonus=0,
                armor_class=25,  # Even high AC doesn't matter
                advantage=AdvantageType.NORMAL,
            )
            result = calculate_attack_roll(request)

            assert result.roll == 20
            assert result.critical_hit is True
            assert result.hit is True  # Natural 20 always hits

    def test_critical_miss_natural_1(self):
        """Test natural 1 is always a critical miss"""
        with patch("random.randint", return_value=1):
            request = AttackRollRequest(
                attack_bonus=50,  # Even high bonus doesn't matter
                armor_class=10,
                advantage=AdvantageType.NORMAL,
            )
            result = calculate_attack_roll(request)

            assert result.roll == 1
            assert result.critical_miss is True
            assert result.hit is False  # Natural 1 always misses

    def test_attack_with_advantage(self):
        """Test attack roll with advantage"""
        with patch("random.randint", side_effect=[8, 15]):
            request = AttackRollRequest(
                attack_bonus=3, armor_class=15, advantage=AdvantageType.ADVANTAGE
            )
            result = calculate_attack_roll(request)

            assert result.roll == 15  # Takes higher roll
            assert result.second_roll == 8
            assert result.total == 18  # 15 + 3
            assert result.hit is True
            assert result.advantage == AdvantageType.ADVANTAGE

    def test_attack_with_disadvantage(self):
        """Test attack roll with disadvantage"""
        with patch("random.randint", side_effect=[15, 8]):
            request = AttackRollRequest(
                attack_bonus=3, armor_class=15, advantage=AdvantageType.DISADVANTAGE
            )
            result = calculate_attack_roll(request)

            assert result.roll == 8  # Takes lower roll
            assert result.second_roll == 15
            assert result.total == 11  # 8 + 3
            assert result.hit is False
            assert result.advantage == AdvantageType.DISADVANTAGE


class TestCalculateDamageRoll:
    """Tests for damage roll calculations"""

    def test_basic_damage_roll(self):
        """Test basic damage roll without critical"""
        with patch("random.randint", side_effect=[3, 5]):
            request = DamageRollRequest(
                damage_dice="2d6+3", damage_type=DamageType.SLASHING, critical_hit=False
            )
            result = calculate_damage_roll(request)

            assert result.rolls == [3, 5]
            assert result.modifier == 3
            assert result.total == 11  # 3 + 5 + 3
            assert result.damage_type == DamageType.SLASHING
            assert result.critical_hit is False

    def test_critical_hit_doubles_dice(self):
        """Test critical hit doubles the number of dice"""
        with patch("random.randint", side_effect=[3, 5, 4, 6]):
            request = DamageRollRequest(
                damage_dice="2d6+3", damage_type=DamageType.PIERCING, critical_hit=True
            )
            result = calculate_damage_roll(request)

            assert len(result.rolls) == 4  # 2d6 becomes 4d6
            assert result.rolls == [3, 5, 4, 6]
            assert result.modifier == 3  # Modifier not doubled
            assert result.total == 21  # 3 + 5 + 4 + 6 + 3
            assert result.critical_hit is True

    def test_damage_with_negative_modifier(self):
        """Test damage roll with negative modifier"""
        with patch("random.randint", return_value=4):
            request = DamageRollRequest(
                damage_dice="1d8-2",
                damage_type=DamageType.BLUDGEONING,
                critical_hit=False,
            )
            result = calculate_damage_roll(request)

            assert result.rolls == [4]
            assert result.modifier == -2
            assert result.total == 2  # 4 - 2

    def test_damage_no_modifier(self):
        """Test damage roll without modifier"""
        with patch("random.randint", side_effect=[2, 4, 3]):
            request = DamageRollRequest(
                damage_dice="3d6", damage_type=DamageType.FIRE, critical_hit=False
            )
            result = calculate_damage_roll(request)

            assert result.rolls == [2, 4, 3]
            assert result.modifier == 0
            assert result.total == 9  # 2 + 4 + 3

    def test_various_damage_types(self):
        """Test different damage types are preserved"""
        damage_types = [
            DamageType.FIRE,
            DamageType.COLD,
            DamageType.LIGHTNING,
            DamageType.NECROTIC,
            DamageType.RADIANT,
        ]

        for dmg_type in damage_types:
            with patch("random.randint", return_value=4):
                request = DamageRollRequest(
                    damage_dice="1d8", damage_type=dmg_type, critical_hit=False
                )
                result = calculate_damage_roll(request)
                assert result.damage_type == dmg_type


class TestCalculateSavingThrow:
    """Tests for saving throw calculations"""

    def test_successful_save(self):
        """Test successful saving throw"""
        with patch("random.randint", return_value=15):
            request = SavingThrowRequest(
                ability_modifier=2,
                proficiency_bonus=3,
                dc=15,
                advantage=AdvantageType.NORMAL,
            )
            result = calculate_saving_throw(request)

            assert result.roll == 15
            assert result.ability_modifier == 2
            assert result.proficiency_bonus == 3
            assert result.total == 20  # 15 + 2 + 3
            assert result.dc == 15
            assert result.success is True
            assert result.natural_20 is False
            assert result.natural_1 is False

    def test_failed_save(self):
        """Test failed saving throw"""
        with patch("random.randint", return_value=5):
            request = SavingThrowRequest(
                ability_modifier=-1,
                proficiency_bonus=0,
                dc=15,
                advantage=AdvantageType.NORMAL,
            )
            result = calculate_saving_throw(request)

            assert result.roll == 5
            assert result.total == 4  # 5 - 1
            assert result.success is False

    def test_natural_20_save(self):
        """Test natural 20 on saving throw"""
        with patch("random.randint", return_value=20):
            request = SavingThrowRequest(
                ability_modifier=0,
                proficiency_bonus=0,
                dc=15,  # Changed to beatable DC
                advantage=AdvantageType.NORMAL,
            )
            result = calculate_saving_throw(request)

            assert result.roll == 20
            assert result.natural_20 is True
            assert result.total == 20
            assert result.success is True  # Succeeds because total >= DC

    def test_natural_1_save(self):
        """Test natural 1 on saving throw"""
        with patch("random.randint", return_value=1):
            request = SavingThrowRequest(
                ability_modifier=0,
                proficiency_bonus=0,
                dc=15,  # Changed to unbeatable DC with nat 1
                advantage=AdvantageType.NORMAL,
            )
            result = calculate_saving_throw(request)

            assert result.roll == 1
            assert result.natural_1 is True
            assert result.total == 1
            assert result.success is False  # Fails because total < DC

    def test_save_with_advantage(self):
        """Test saving throw with advantage"""
        with patch("random.randint", side_effect=[8, 15]):
            request = SavingThrowRequest(
                ability_modifier=2,
                proficiency_bonus=2,
                dc=15,
                advantage=AdvantageType.ADVANTAGE,
            )
            result = calculate_saving_throw(request)

            assert result.roll == 15  # Takes higher roll
            assert result.second_roll == 8
            assert result.total == 19  # 15 + 2 + 2
            assert result.success is True


class TestCalculateFullCombat:
    """Tests for full combat calculation (attack + damage)"""

    def test_successful_hit_with_damage(self):
        """Test complete combat where attack hits"""
        with patch("random.randint", side_effect=[15, 4, 6]):
            # 15 for attack roll, [4, 6] for damage (2d6)
            request = CombatCalculatorRequest(
                attack_bonus=5,
                armor_class=15,
                damage_dice="2d6+3",
                damage_type=DamageType.SLASHING,
                advantage=AdvantageType.NORMAL,
            )
            result = calculate_full_combat(request)

            # Check attack
            assert result.attack.roll == 15
            assert result.attack.total == 20
            assert result.attack.hit is True

            # Check damage
            assert result.damage is not None
            assert result.damage.rolls == [4, 6]
            assert result.damage.total == 13  # 4 + 6 + 3

    def test_missed_attack_no_damage(self):
        """Test combat where attack misses (no damage calculated)"""
        with patch("random.randint", return_value=5):
            request = CombatCalculatorRequest(
                attack_bonus=2,
                armor_class=15,
                damage_dice="2d6+3",
                damage_type=DamageType.PIERCING,
                advantage=AdvantageType.NORMAL,
            )
            result = calculate_full_combat(request)

            # Check attack
            assert result.attack.roll == 5
            assert result.attack.hit is False

            # No damage on miss
            assert result.damage is None

    def test_critical_hit_doubles_damage_dice(self):
        """Test critical hit doubles damage dice in full combat"""
        with patch("random.randint", side_effect=[20, 3, 5, 4, 6]):
            # 20 for crit, [3, 5, 4, 6] for 4d6 (doubled)
            request = CombatCalculatorRequest(
                attack_bonus=5,
                armor_class=15,
                damage_dice="2d6+3",
                damage_type=DamageType.SLASHING,
                advantage=AdvantageType.NORMAL,
            )
            result = calculate_full_combat(request)

            # Check critical hit
            assert result.attack.critical_hit is True

            # Check doubled damage dice
            assert result.damage is not None
            assert len(result.damage.rolls) == 4  # 2d6 becomes 4d6
            assert result.damage.critical_hit is True
            assert result.damage.total == 21  # 3 + 5 + 4 + 6 + 3

    def test_critical_miss_no_damage(self):
        """Test critical miss (natural 1) results in no damage"""
        with patch("random.randint", return_value=1):
            request = CombatCalculatorRequest(
                attack_bonus=10,
                armor_class=10,
                damage_dice="2d6+3",
                damage_type=DamageType.BLUDGEONING,
                advantage=AdvantageType.NORMAL,
            )
            result = calculate_full_combat(request)

            assert result.attack.critical_miss is True
            assert result.attack.hit is False
            assert result.damage is None

    def test_combat_with_advantage(self):
        """Test full combat with advantage"""
        with patch("random.randint", side_effect=[8, 18, 5, 3]):
            # [8, 18] for advantage, [5, 3] for 2d6 damage
            request = CombatCalculatorRequest(
                attack_bonus=3,
                armor_class=15,
                damage_dice="2d6+2",
                damage_type=DamageType.PIERCING,
                advantage=AdvantageType.ADVANTAGE,
            )
            result = calculate_full_combat(request)

            assert result.attack.roll == 18  # Higher roll
            assert result.attack.second_roll == 8
            assert result.attack.hit is True
            assert result.damage is not None
            assert result.damage.total == 10  # 5 + 3 + 2
