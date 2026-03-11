from fastapi import APIRouter, Query, HTTPException
import random

from app.models import SpellsResponse, SpellSchool, Spell
from app.services.data_loader import load_spells
from app.services.spell_service import generate_random_spell
from app.services.query_utils import filter_records, paginate_records
from app.api.dependencies import CommonSearch, CommonSpellLevel

router = APIRouter()


@router.get("", response_model=SpellsResponse)
def get_spells(
    search: CommonSearch,
    level_params: CommonSpellLevel,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    school: SpellSchool | None = Query(None, description="Filter by school of magic"),
    spell_class: str | None = Query(None, description="Filter by class (e.g. Wizard, Cleric)"),
    concentration: bool | None = Query(None, description="Filter by concentration requirement"),
    ritual: bool | None = Query(None, description="Filter by ritual casting"),
):
    """
    Return all D&D spells with optional filtering and pagination.

    Filters:
    - name: Search by name (partial match, case-insensitive)
    - school: School of magic (e.g. Evocation, Necromancy)
    - min_level / max_level: Spell level range (0 = cantrip)
    - spell_class: Class that can cast the spell (e.g. Wizard, Cleric)
    - concentration: Whether the spell requires concentration
    - ritual: Whether the spell can be cast as a ritual

    Pagination:
    - skip: Number of records to skip (default: 0)
    - limit: Maximum records to return (default: 10, max: 100)
    """
    spells = load_spells()

    predicates = []
    if search.name:
        name_filter = search.name.lower()
        predicates.append(lambda s: name_filter in s["name"].lower())
    if school:
        school_val = school.value
        predicates.append(lambda s: s["school"] == school_val)
    if level_params.min_level is not None:
        min_l = level_params.min_level
        predicates.append(lambda s: s["level"] >= min_l)
    if level_params.max_level is not None:
        max_l = level_params.max_level
        predicates.append(lambda s: s["level"] <= max_l)
    if spell_class:
        class_filter = spell_class.lower()
        predicates.append(lambda s: any(class_filter == c.lower() for c in s["classes"]))
    if concentration is not None:
        conc_val = concentration
        predicates.append(lambda s: s["concentration"] == conc_val)
    if ritual is not None:
        ritual_val = ritual
        predicates.append(lambda s: s["ritual"] == ritual_val)

    filtered = filter_records(spells, predicates)
    paginated, total = paginate_records(filtered, skip, limit)

    return {"spells": paginated, "total": total, "skip": skip, "limit": limit}


@router.get("/random", response_model=Spell)
def get_random_spell(
    level_params: CommonSpellLevel,
    school: SpellSchool | None = Query(None, description="School of magic"),
    spell_class: str | None = Query(None, description="Class that can cast the spell"),
):
    """Generate a random D&D spell with optional constraints."""
    level = None
    if level_params.min_level is not None or level_params.max_level is not None:
        min_l = level_params.min_level if level_params.min_level is not None else 0
        max_l = level_params.max_level if level_params.max_level is not None else 9
        level = random.randint(min_l, max_l)

    return generate_random_spell(school=school, level=level, spell_class=spell_class)


@router.get("/{spell_id}", response_model=Spell)
def get_spell(spell_id: int):
    """Return a single spell by ID."""
    spells = load_spells()
    spell = next((s for s in spells if s["id"] == spell_id), None)
    if not spell:
        raise HTTPException(status_code=404, detail=f"Spell with id {spell_id} not found")
    return spell
