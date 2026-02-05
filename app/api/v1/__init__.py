"""API v1 router aggregation"""

from fastapi import APIRouter
from app.api.v1 import characters, monsters, game_data, items

# Create a main router for v1
api_router = APIRouter()

# Include all v1 routers
api_router.include_router(characters.router, prefix="/characters", tags=["characters"])
api_router.include_router(monsters.router, prefix="/monsters", tags=["monsters"])
api_router.include_router(game_data.router, tags=["game-data"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
