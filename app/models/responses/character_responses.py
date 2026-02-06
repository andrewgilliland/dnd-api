"""Character response models"""

from pydantic import BaseModel
from app.models.character import Character, Class, Race


class CharactersResponse(BaseModel):
    """Response model for multiple characters"""

    characters: list[Character]


class ClassResponse(BaseModel):
    """Response model for character classes"""

    classes: list[Class]


class RaceResponse(BaseModel):
    """Response model for character races"""

    races: list[Race]
