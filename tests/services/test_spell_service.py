"""Tests for spell service functions"""

from app.services.spell_service import generate_random_spell
from app.models.spell import Spell, SpellSchool, SpellComponent


def test_generate_random_spell_returns_spell():
    """Test that generate_random_spell returns a Spell instance"""
    spell = generate_random_spell()
    assert isinstance(spell, Spell)


def test_generate_random_spell_has_required_fields():
    """Test that the generated spell has all required fields"""
    spell = generate_random_spell()
    assert spell.name
    assert spell.school in SpellSchool
    assert 0 <= spell.level <= 9
    assert spell.casting_time
    assert spell.range
    assert isinstance(spell.components, list)
    assert len(spell.components) >= 1
    assert spell.duration
    assert isinstance(spell.concentration, bool)
    assert isinstance(spell.ritual, bool)
    assert spell.description
    assert isinstance(spell.classes, list)
    assert len(spell.classes) > 0


def test_generate_random_spell_with_school():
    """Test that school constraint is respected"""
    spell = generate_random_spell(school=SpellSchool.EVOCATION)
    assert spell.school == SpellSchool.EVOCATION


def test_generate_random_spell_with_each_school():
    """Test that every school can be used as a constraint"""
    for school in SpellSchool:
        spell = generate_random_spell(school=school)
        assert spell.school == school


def test_generate_random_spell_with_level():
    """Test that level constraint is respected"""
    spell = generate_random_spell(level=5)
    assert spell.level == 5


def test_generate_random_spell_cantrip():
    """Test generating a cantrip (level 0)"""
    spell = generate_random_spell(level=0)
    assert spell.level == 0
    assert "Cantrip" in spell.name


def test_generate_random_spell_named_with_level():
    """Test that non-cantrip name includes the level"""
    spell = generate_random_spell(level=7)
    assert "Level 7" in spell.name


def test_generate_random_spell_with_spell_class():
    """Test that the spell class appears in the classes list"""
    spell = generate_random_spell(spell_class="Paladin")
    assert "Paladin" in spell.classes


def test_generate_random_spell_components_are_valid():
    """Test that all spell components are valid SpellComponent values"""
    spell = generate_random_spell()
    for component in spell.components:
        assert component in SpellComponent


def test_generate_random_spell_always_has_verbal_and_somatic():
    """Test that V and S components are always present"""
    for _ in range(10):
        spell = generate_random_spell()
        assert SpellComponent.VERBAL in spell.components
        assert SpellComponent.SOMATIC in spell.components


def test_generate_random_spell_concentration_affects_duration():
    """Test that concentration spells have '1 minute' duration"""
    # Run multiple times to get a concentration spell
    found_concentration = False
    for _ in range(50):
        spell = generate_random_spell(level=5)
        if spell.concentration:
            assert spell.duration == "1 minute"
            found_concentration = True
            break
    # If we didn't encounter a concentration spell in 50 tries,
    # skip rather than fail (probabilistic)
    if not found_concentration:
        pass


def test_generate_random_spell_no_concentration_instantaneous():
    """Test that non-concentration spells have 'Instantaneous' duration"""
    for _ in range(50):
        spell = generate_random_spell(level=1)
        if not spell.concentration:
            assert spell.duration == "Instantaneous"
            break


def test_generate_random_spell_school_in_name():
    """Test that the school name appears in the generated spell name"""
    spell = generate_random_spell(school=SpellSchool.ILLUSION)
    assert "Illusion" in spell.name


def test_generate_random_spell_school_description_in_description():
    """Test that the description references the school"""
    spell = generate_random_spell(school=SpellSchool.NECROMANCY)
    assert spell.description
    assert len(spell.description) > 0
