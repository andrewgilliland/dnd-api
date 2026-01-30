from fastapi import APIRouter, Query

from app.models import CharactersResponse, Class, Race
from app.services.data_loader import load_characters

router = APIRouter(prefix="/characters", tags=["characters"])


@router.get("", response_model=CharactersResponse)
def get_characters(
    class_: Class | None = Query(
        None, alias="class", description="Filter by character class"
    ),
    race: Race | None = Query(None, description="Filter by character race"),
    name: str | None = Query(None, description="Search by name (case-insensitive)"),
):
    """
    Return all D&D characters from Dragonlance with optional filtering.

    Filters:
    - class: Character class (e.g., Fighter, Wizard, Cleric)
    - race: Character race (e.g., Human, Elf, Dwarf)
    - name: Search by name (partial match, case-insensitive)
    """
    characters = load_characters()

    # Apply filters
    if class_:
        characters = [c for c in characters if c["class"] == class_.value]

    if race:
        characters = [c for c in characters if c["race"] == race.value]

    if name:
        characters = [c for c in characters if name.lower() in c["name"].lower()]

    return {"characters": characters}
