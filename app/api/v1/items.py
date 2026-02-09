from fastapi import APIRouter, Query, HTTPException

from app.models import ItemsResponse, Item, ItemType, Rarity
from app.services.data_loader import load_items
from app.api.dependencies import CommonSearch, CommonCostRange

router = APIRouter()


@router.get("", response_model=ItemsResponse)
def get_items(
    search: CommonSearch,
    cost_range: CommonCostRange,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of records to return"
    ),
    type: ItemType | None = Query(None, description="Filter by item type"),
    rarity: Rarity | None = Query(None, description="Filter by item rarity"),
    magic: bool | None = Query(None, description="Filter by magic items (true/false)"),
    attunement: bool | None = Query(
        None, description="Filter by attunement requirement (true/false)"
    ),
):
    """
    Return all D&D items and equipment with optional filtering and pagination.

    Filters:
    - type: Item type (e.g., Weapon, Armor, Potion, Wondrous Item)
    - rarity: Item rarity (e.g., Common, Uncommon, Rare, Very Rare, Legendary)
    - magic: Whether the item is magical (true/false)
    - attunement: Whether the item requires attunement (true/false)
    - min_cost: Minimum cost in gold pieces
    - max_cost: Maximum cost in gold pieces
    - name: Search by name (partial match, case-insensitive)

    Pagination:
    - skip: Number of records to skip (default: 0)
    - limit: Maximum records to return (default: 10, max: 100)
    """
    items = load_items()

    # Apply filters
    if type:
        items = [i for i in items if i["type"] == type.value]

    if rarity:
        items = [i for i in items if i["rarity"] == rarity.value]

    if magic is not None:
        items = [i for i in items if i["magic"] == magic]

    if attunement is not None:
        items = [i for i in items if i["attunement_required"] == attunement]

    if cost_range.min_cost is not None:
        items = [i for i in items if i["cost"] >= cost_range.min_cost]

    if cost_range.max_cost is not None:
        items = [i for i in items if i["cost"] <= cost_range.max_cost]

    if search.name:
        items = [i for i in items if search.name.lower() in i["name"].lower()]

    # Get total count before pagination
    total = len(items)

    # Apply pagination
    paginated_items = items[skip : skip + limit]

    return {
        "items": paginated_items,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/{item_id}", response_model=Item)
def get_item_by_id(item_id: int):
    """
    Get a single item by ID.

    Returns:
    - Item details if found
    - 404 error if item not found
    """
    items = load_items()
    item = next((i for i in items if i["id"] == item_id), None)

    if not item:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")

    return item
