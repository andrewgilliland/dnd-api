"""Dependency injection functions for FastAPI routes"""

from typing import Annotated
from fastapi import Depends, Query
from app.config import settings
from app.config.settings import Settings


# Common Query Parameter Dependencies
class PaginationParams:
    """Common pagination parameters"""

    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(
            100, ge=1, le=1000, description="Maximum number of records to return"
        ),
    ):
        self.skip = skip
        self.limit = limit


class SearchParams:
    """Common search parameters"""

    def __init__(
        self,
        name: str | None = Query(None, description="Search by name (case-insensitive)"),
    ):
        self.name = name


class ChallengeRatingParams:
    """Challenge rating filter parameters"""

    def __init__(
        self,
        min_cr: float | None = Query(
            None, ge=0, description="Minimum challenge rating"
        ),
        max_cr: float | None = Query(
            None, ge=0, description="Maximum challenge rating"
        ),
    ):
        self.min_cr = min_cr
        self.max_cr = max_cr


class CostRangeParams:
    """Cost range filter parameters"""

    def __init__(
        self,
        min_cost: int | None = Query(None, ge=0, description="Minimum cost in gold"),
        max_cost: int | None = Query(None, ge=0, description="Maximum cost in gold"),
    ):
        self.min_cost = min_cost
        self.max_cost = max_cost


class SpellLevelParams:
    """Spell level filter parameters"""

    def __init__(
        self,
        min_level: int | None = Query(None, ge=0, le=9, description="Minimum spell level (0=cantrip)"),
        max_level: int | None = Query(None, ge=0, le=9, description="Maximum spell level (0=cantrip)"),
    ):
        self.min_level = min_level
        self.max_level = max_level


# Settings Dependency
def get_settings() -> Settings:
    """Get application settings"""
    return settings


# Type Aliases for cleaner dependency injection
CommonPagination = Annotated[PaginationParams, Depends(PaginationParams)]
CommonSearch = Annotated[SearchParams, Depends(SearchParams)]
CommonChallengeRating = Annotated[ChallengeRatingParams, Depends(ChallengeRatingParams)]
CommonCostRange = Annotated[CostRangeParams, Depends(CostRangeParams)]
CommonSpellLevel = Annotated[SpellLevelParams, Depends(SpellLevelParams)]
CommonSettings = Annotated[Settings, Depends(get_settings)]
