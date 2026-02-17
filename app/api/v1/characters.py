from fastapi import APIRouter, Query, HTTPException

from app.models import CharactersResponse, Class, Race, Character
from app.services.data_loader import load_characters
from app.services.character_service import generate_random_character
from app.services.query_utils import filter_records, paginate_records
from app.api.dependencies import CommonSearch

router = APIRouter()


@router.get("", response_model=CharactersResponse)
def get_characters(
    search: CommonSearch,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    class_: Class | None = Query(
        None, alias="class", description="Filter by character class"
    ),
    race: Race | None = Query(None, description="Filter by character race"),
):
    """
    Return all D&D characters from Dragonlance with optional filtering and pagination.

    Filters:
    - class: Character class (e.g., Fighter, Wizard, Cleric)
    - race: Character race (e.g., Human, Elf, Dwarf)
    - name: Search by name (partial match, case-insensitive)
    
    Pagination:
    - skip: Number of records to skip (default: 0)
    - limit: Maximum records to return (default: 10, max: 100)
    """
    characters = load_characters()

    predicates = []
    if class_:
        predicates.append(lambda character: character["class"] == class_.value)
    if race:
        predicates.append(lambda character: character["race"] == race.value)
    if search.name:
        name_filter = search.name.lower()
        predicates.append(lambda character: name_filter in character["name"].lower())

    filtered_characters = filter_records(characters, predicates)
    paginated_characters, total = paginate_records(filtered_characters, skip, limit)

    return {
        "characters": paginated_characters,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


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
