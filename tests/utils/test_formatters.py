"""Tests for utility functions - formatters"""

import pytest
from app.utils.formatters import format_modifier, pluralize, titlecase


def test_format_modifier_positive():
    """Test formatting positive modifiers"""
    assert format_modifier(3) == "+3"
    assert format_modifier(10) == "+10"


def test_format_modifier_negative():
    """Test formatting negative modifiers"""
    assert format_modifier(-2) == "-2"
    assert format_modifier(-5) == "-5"


def test_format_modifier_zero():
    """Test formatting zero modifier"""
    assert format_modifier(0) == "+0"


def test_pluralize_singular():
    """Test pluralize with singular count"""
    assert pluralize(1, "monster") == "1 monster"
    assert pluralize(1, "wolf", "wolves") == "1 wolf"


def test_pluralize_plural():
    """Test pluralize with plural count"""
    assert pluralize(2, "monster") == "2 monsters"
    assert pluralize(5, "wolf", "wolves") == "5 wolves"


def test_pluralize_zero():
    """Test pluralize with zero count"""
    assert pluralize(0, "monster") == "0 monsters"


def test_titlecase_basic():
    """Test basic title case"""
    assert titlecase("the quick brown fox") == "The Quick Brown Fox"


def test_titlecase_with_lowercase_words():
    """Test title case preserving certain lowercase words"""
    assert titlecase("the lord of the rings") == "The Lord of the Rings"
    assert titlecase("a tale of two cities") == "A Tale of Two Cities"


def test_titlecase_first_word_capitalized():
    """Test that first word is always capitalized"""
    assert titlecase("the beginning") == "The Beginning"
    assert titlecase("a start") == "A Start"
