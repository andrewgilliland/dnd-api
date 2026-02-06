from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router as api_v1_router
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
        "docs": "/docs",
        "api_v1": "/api/v1",
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring and load balancers"""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "version": settings.api_version,
    }


# Include API v1 router
app.include_router(api_v1_router, prefix="/api/v1")
