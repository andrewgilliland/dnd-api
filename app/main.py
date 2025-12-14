import json
from pathlib import Path
from fastapi import FastAPI

from app.models import CharactersResponse, ClassResponse, Class, Race

app = FastAPI(title="D&D API")


@app.get("/")
def root():
    return {"message": "Welcome to the D&D API"}


@app.get("/classes", response_model=ClassResponse)
def get_classes():
    """Return all D&D 5e character classes"""
    return {"classes": [cls.value for cls in Class]}


@app.get("/races")
def get_races():
    """Return all D&D 5e character races"""
    return {"races": [race.value for race in Race]}


@app.get("/characters", response_model=CharactersResponse)
def get_characters():
    """Return all D&D characters from Dragonlance"""
    characters_file = Path(__file__).parent / "characters.json"
    with open(characters_file, "r") as f:
        characters = json.load(f)
    return {"characters": characters}
