from fastapi import APIRouter, Query, HTTPException

from app.models import ItemsResponse, Item, ItemType, Rarity
from app.services.data_loader import load_items
from app.services.query_utils import filter_records, paginate_records
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

    predicates = []
    if type:
        predicates.append(lambda item: item["type"] == type.value)
    if rarity:
        predicates.append(lambda item: item["rarity"] == rarity.value)
    if magic is not None:
        predicates.append(lambda item: item["magic"] == magic)
    if attunement is not None:
        predicates.append(
            lambda item: item["attunement_required"] == attunement
        )
    if cost_range.min_cost is not None:
        predicates.append(lambda item: item["cost"] >= cost_range.min_cost)
    if cost_range.max_cost is not None:
        predicates.append(lambda item: item["cost"] <= cost_range.max_cost)
    if search.name:
        name_filter = search.name.lower()
        predicates.append(lambda item: name_filter in item["name"].lower())

    filtered_items = filter_records(items, predicates)
    paginated_items, total = paginate_records(filtered_items, skip, limit)

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
