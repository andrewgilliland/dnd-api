from fastapi import APIRouter, Query, HTTPException

from app.models import CharactersResponse, Class, Race, Character
from app.services.data_loader import load_characters
from app.services.character_service import generate_random_character

router = APIRouter()


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


@router.get("/random", response_model=Character)
def get_random_character():
    """
    Generate a random D&D character.

    Returns:
    - A randomly generated character with:
      - Random race, class, and alignment
      - Random ability scores (4d6 drop lowest)
      - Generated name and description
    """
    return generate_random_character()


@router.get("/{character_id}", response_model=Character)
def get_character_by_id(character_id: int):
    """
    Get a single character by ID.

    Returns:
    - Character details if found
    - 404 error if character not found
    """
    characters = load_characters()
    character = next((c for c in characters if c["id"] == character_id), None)

    if not character:
        raise HTTPException(
            status_code=404, detail=f"Character with id {character_id} not found"
        )

    return character
