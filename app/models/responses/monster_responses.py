"""Monster response models"""

from pydantic import BaseModel
from app.models.monster import Monster


class MonstersResponse(BaseModel):
    """Response model for multiple monsters"""

    monsters: list[Monster]
    total: int
    skip: int
    limit: int
