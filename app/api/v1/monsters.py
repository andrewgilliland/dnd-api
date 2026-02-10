from fastapi import APIRouter, Query, HTTPException

from app.models import MonstersResponse, MonsterType, Size, Monster
from app.services.data_loader import load_monsters
from app.services.monster_service import generate_random_monster
from app.api.dependencies import CommonSearch, CommonChallengeRating

router = APIRouter()


@router.get("", response_model=MonstersResponse)
def get_monsters(
    search: CommonSearch,
    cr_params: CommonChallengeRating,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of records to return"
    ),
    type: MonsterType | None = Query(None, description="Filter by monster type"),
    size: Size | None = Query(None, description="Filter by monster size"),
):
    """
    Return all D&D monsters with optional filtering and pagination.

    Filters:
    - type: Monster type (e.g., Dragon, Beast, Humanoid)
    - size: Monster size (e.g., Tiny, Small, Medium, Large, Huge, Gargantuan)
    - min_cr: Minimum challenge rating
    - max_cr: Maximum challenge rating
    - name: Search by name (partial match, case-insensitive)

    Pagination:
    - skip: Number of records to skip (default: 0)
    - limit: Maximum records to return (default: 10, max: 100)
    """
    monsters = load_monsters()

    # Apply filters
    if type:
        monsters = [m for m in monsters if m["type"] == type.value]

    if size:
        monsters = [m for m in monsters if m["size"] == size.value]

    if cr_params.min_cr is not None:
        monsters = [m for m in monsters if m["challenge_rating"] >= cr_params.min_cr]

    if cr_params.max_cr is not None:
        monsters = [m for m in monsters if m["challenge_rating"] <= cr_params.max_cr]

    if search.name:
        monsters = [m for m in monsters if search.name.lower() in m["name"].lower()]

    # Get total count before pagination
    total = len(monsters)

    # Apply pagination
    paginated_monsters = monsters[skip : skip + limit]

    return {
        "monsters": paginated_monsters,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/random", response_model=Monster)
def get_random_monster(
    cr_params: CommonChallengeRating,
    type: MonsterType | None = Query(None, description="Filter by monster type"),
    size: Size | None = Query(None, description="Filter by monster size"),
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
        monster_type=type, size=size, min_cr=cr_params.min_cr, max_cr=cr_params.max_cr
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
