"""Party response models"""

from pydantic import BaseModel
from app.models.party import Party


class PartiesResponse(BaseModel):
    """Response model for multiple parties"""

    parties: list[Party]
    total: int
    skip: int
    limit: int
