from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import characters, monsters, game_data
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    debug=settings.debug,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to the D&D API",
        "environment": settings.environment,
        "version": settings.api_version,
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring and load balancers"""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "version": settings.api_version,
    }


# Include routers
app.include_router(characters.router)
app.include_router(monsters.router)
app.include_router(game_data.router)
