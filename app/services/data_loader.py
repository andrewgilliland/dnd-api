from functools import lru_cache
import json
from pathlib import Path


@lru_cache(maxsize=1)
def load_monsters():
    """Load and cache monster data to avoid reading file on every request"""
    file_path = Path(__file__).parent.parent / "data" / "monsters.json"
    with open(file_path, "r") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_characters():
    """Load and cache character data to avoid reading file on every request"""
    file_path = Path(__file__).parent.parent / "data" / "characters.json"
    with open(file_path, "r") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_items():
    """Load and cache items data to avoid reading file on every request"""
    file_path = Path(__file__).parent.parent / "data" / "items.json"
    with open(file_path, "r") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_character_names():
    """Load and cache character names data"""
    file_path = Path(__file__).parent.parent / "data" / "character_names.json"
    with open(file_path, "r") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_character_traits():
    """Load and cache character traits data"""
    file_path = Path(__file__).parent.parent / "data" / "character_traits.json"
    with open(file_path, "r") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_monster_names():
    """Load and cache monster names data"""
    file_path = Path(__file__).parent.parent / "data" / "monster_names.json"
    with open(file_path, "r") as f:
        return json.load(f)
