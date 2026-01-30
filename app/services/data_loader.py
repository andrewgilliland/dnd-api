from functools import lru_cache
import json
from pathlib import Path


@lru_cache(maxsize=1)
def load_monsters():
    """Load and cache monster data to avoid reading file on every request"""
    file_path = Path(__file__).parent.parent / "monsters.json"
    with open(file_path, "r") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_characters():
    """Load and cache character data to avoid reading file on every request"""
    file_path = Path(__file__).parent.parent / "characters.json"
    with open(file_path, "r") as f:
        return json.load(f)
