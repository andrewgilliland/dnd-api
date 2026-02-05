from fastapi import APIRouter

from app.models import ClassResponse, Class, Race

router = APIRouter()


@router.get("/classes", response_model=ClassResponse)
def get_classes():
    """Return all D&D 5e character classes"""
    return {"classes": [cls.value for cls in Class]}


@router.get("/races")
def get_races():
    """Return all D&D 5e character races"""
    return {"races": [race.value for race in Race]}
