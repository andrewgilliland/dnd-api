"""Spell response models"""

from pydantic import BaseModel
from app.models.spell import Spell


class SpellsResponse(BaseModel):
    """Response model for multiple spells"""

    spells: list[Spell]
    total: int
    skip: int
    limit: int
