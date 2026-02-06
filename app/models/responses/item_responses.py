"""Item response models"""

from pydantic import BaseModel
from app.models.item import Item


class ItemsResponse(BaseModel):
    """Response model for multiple items"""

    items: list[Item]
