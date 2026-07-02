"""Party endpoints"""

from datetime import datetime
from fastapi import APIRouter, Query
from app.models.party import (
    Party,
    PartyMember,
    PartyStatus,
    PartyRole,
    CreatePartyRequest,
)
from app.models.responses.party_responses import PartiesResponse

router = APIRouter()

# Mock data for parties
MOCK_PARTIES = [
    Party(
        id="party-1",
        name="Stormbreakers",
        created_by_user_id="user-1",
        status=PartyStatus.ACTIVE,
        members=[
            PartyMember(
                character_id=1,
                role=PartyRole.TANK,
                is_leader=True,
                marching_order=1,
                joined_at=datetime.now().isoformat(),
            ),
            PartyMember(
                character_id=2,
                role=PartyRole.HEALER,
                is_leader=False,
                marching_order=2,
                joined_at=datetime.now().isoformat(),
            ),
            PartyMember(
                character_id=3,
                role=PartyRole.CASTER,
                is_leader=False,
                marching_order=3,
                joined_at=datetime.now().isoformat(),
            ),
        ],
        notes="Weekly campaign party from Dragonlance setting",
        tags=["weekly", "dragonlance", "heroic"],
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
    ),
    Party(
        id="party-2",
        name="Shadow Runners",
        created_by_user_id="user-2",
        status=PartyStatus.ACTIVE,
        members=[
            PartyMember(
                character_id=4,
                role=PartyRole.SCOUT,
                is_leader=True,
                marching_order=1,
                joined_at=datetime.now().isoformat(),
            ),
            PartyMember(
                character_id=5,
                role=PartyRole.STRIKER,
                is_leader=False,
                marching_order=2,
                joined_at=datetime.now().isoformat(),
            ),
        ],
        notes="Urban intrigue campaign",
        tags=["urban", "intrigue"],
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
    ),
]


@router.get("", response_model=PartiesResponse)
def get_parties(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of records to return"
    ),
    name: str | None = Query(None, description="Filter by party name (partial match)"),
):
    """
    Get all parties with optional filtering and pagination.

    Filters:
    - name: Search by party name (partial match, case-insensitive)

    Pagination:
    - skip: Number of records to skip (default: 0)
    - limit: Maximum records to return (default: 10, max: 100)
    """
    filtered_parties = MOCK_PARTIES

    if name:
        name_lower = name.lower()
        filtered_parties = [
            party for party in filtered_parties if name_lower in party.name.lower()
        ]

    total = len(filtered_parties)
    paginated = filtered_parties[skip : skip + limit]

    return {
        "parties": paginated,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.post("", response_model=Party)
def create_party(request: CreatePartyRequest):
    """
    Create a new party.

    Returns:
    - The created party with generated ID and timestamps
    """
    now = datetime.now().isoformat()

    # Convert request members to PartyMember objects
    members = [
        PartyMember(
            character_id=member.get("characterId"),
            role=PartyRole(member.get("role")) if member.get("role") else None,
            is_leader=member.get("isLeader", False),
            marching_order=member.get("marchingOrder", 0),
            joined_at=now,
        )
        for member in request.members
    ]

    party = Party(
        id=f"party-{len(MOCK_PARTIES) + 1}",
        name=request.name,
        created_by_user_id="current-user",
        status=PartyStatus.ACTIVE,
        members=members,
        notes=request.notes,
        tags=request.tags,
        created_at=now,
        updated_at=now,
    )

    # In a real app, save to DB
    MOCK_PARTIES.append(party)

    return party
