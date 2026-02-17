"""Shared query utilities for filtering and pagination."""

from collections.abc import Callable
from typing import Any


Record = dict[str, Any]
Predicate = Callable[[Record], bool]


def filter_records(records: list[Record], predicates: list[Predicate]) -> list[Record]:
    """Apply predicates in order and return filtered records."""
    filtered_records = records
    for predicate in predicates:
        filtered_records = [record for record in filtered_records if predicate(record)]
    return filtered_records


def paginate_records(records: list[Record], skip: int, limit: int) -> tuple[list[Record], int]:
    """Return paginated records and total count before pagination."""
    total_records = len(records)
    paginated_records = records[skip : skip + limit]
    return paginated_records, total_records
