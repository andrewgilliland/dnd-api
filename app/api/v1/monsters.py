from fastapi import APIRouter, Query, HTTPException

from app.models import MonstersResponse, MonsterType, Size, Monster
from app.services.data_loader import load_monsters
from app.services.monster_service import generate_random_monster

router = APIRouter()


@router.get("", response_model=MonstersResponse)
def get_monsters(
    type: MonsterType | None = Query(None, description="Filter by monster type"),
    size: Size | None = Query(None, description="Filter by monster size"),
    min_cr: float | None = Query(None, ge=0, description="Minimum challenge rating"),
    max_cr: float | None = Query(None, ge=0, description="Maximum challenge rating"),
    name: str | None = Query(None, description="Search by name (case-insensitive)"),
):
    """
    Return all D&D monsters with optional filtering.

    Filters:
    - type: Monster type (e.g., Dragon, Beast, Humanoid)
    - size: Monster size (e.g., Tiny, Small, Medium, Large, Huge, Gargantuan)
    - min_cr: Minimum challenge rating
    - max_cr: Maximum challenge rating
    - name: Search by name (partial match, case-insensitive)
    """
    monsters = load_monsters()

    # Apply filters
    if type:
        monsters = [m for m in monsters if m["type"] == type.value]

    if size:
        monsters = [m for m in monsters if m["size"] == size.value]

    if min_cr is not None:
        monsters = [m for m in monsters if m["challenge_rating"] >= min_cr]

    if max_cr is not None:
        monsters = [m for m in monsters if m["challenge_rating"] <= max_cr]

    if name:
        monsters = [m for m in monsters if name.lower() in m["name"].lower()]

    return {"monsters": monsters}


@router.get("/random", response_model=Monster)
def get_random_monster(
    type: MonsterType | None = Query(None, description="Filter by monster type"),
    size: Size | None = Query(None, description="Filter by monster size"),
    min_cr: float | None = Query(None, ge=0, description="Minimum challenge rating"),
    max_cr: float | None = Query(None, ge=0, description="Maximum challenge rating"),
):
    """
    Generate a random D&D monster.

    Optional Filters:
    - type: Monster type (e.g., Dragon, Beast, Humanoid)
    - size: Monster size (e.g., Tiny, Small, Medium, Large)
    - min_cr: Minimum challenge rating
    - max_cr: Maximum challenge rating

    Returns:
    - A randomly generated monster with:
      - Random or filtered type and size
      - Challenge rating within specified range
      - Appropriate stats, HP, AC, and actions for its CR
      - Random alignment and abilities
    """
    return generate_random_monster(
        monster_type=type, size=size, min_cr=min_cr, max_cr=max_cr
    )


@router.get("/{monster_id}", response_model=Monster)
def get_monster_by_id(monster_id: int):
    """
    Get a single monster by ID.

    Returns:
    - Monster details if found
    - 404 error if monster not found
    """
    monsters = load_monsters()
    monster = next((m for m in monsters if m["id"] == monster_id), None)

    if not monster:
        raise HTTPException(
            status_code=404, detail=f"Monster with id {monster_id} not found"
        )

    return monster
