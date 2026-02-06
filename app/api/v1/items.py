from fastapi import APIRouter, Query, HTTPException

from app.models import ItemsResponse, Item, ItemType, Rarity
from app.services.data_loader import load_items

router = APIRouter()


@router.get("", response_model=ItemsResponse)
def get_items(
    type: ItemType | None = Query(None, description="Filter by item type"),
    rarity: Rarity | None = Query(None, description="Filter by item rarity"),
    magic: bool | None = Query(None, description="Filter by magic items (true/false)"),
    attunement: bool | None = Query(
        None, description="Filter by attunement requirement (true/false)"
    ),
    min_cost: int | None = Query(None, ge=0, description="Minimum cost in gold"),
    max_cost: int | None = Query(None, ge=0, description="Maximum cost in gold"),
    name: str | None = Query(None, description="Search by name (case-insensitive)"),
):
    """
    Return all D&D items and equipment with optional filtering.

    Filters:
    - type: Item type (e.g., Weapon, Armor, Potion, Wondrous Item)
    - rarity: Item rarity (e.g., Common, Uncommon, Rare, Very Rare, Legendary)
    - magic: Whether the item is magical (true/false)
    - attunement: Whether the item requires attunement (true/false)
    - min_cost: Minimum cost in gold pieces
    - max_cost: Maximum cost in gold pieces
    - name: Search by name (partial match, case-insensitive)
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

    if min_cost is not None:
        items = [i for i in items if i["cost"] >= min_cost]

    if max_cost is not None:
        items = [i for i in items if i["cost"] <= max_cost]

    if name:
        items = [i for i in items if name.lower() in i["name"].lower()]

    return {"items": items}


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
