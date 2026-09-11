"""Finite RFC 8785 canonical byte helpers shared by CP-002 contracts."""

from __future__ import annotations

from typing import Any

import rfc8785

from .errors import CanonicalizationError

SAFE_INTEGER_MAX = 9_007_199_254_740_991
SAFE_INTEGER_MIN = -SAFE_INTEGER_MAX
MAX_CONTAINER_DEPTH = 32
MAX_MAPPING_ENTRIES = 256
MAX_SEQUENCE_ELEMENTS = 256
MAX_AGGREGATE_NODES = 4_096
MAX_STRING_SCALARS = 16_384


def canonical_json_bytes(value: Any) -> bytes:
    """Return RFC 8785 JCS UTF-8 bytes without reflecting rejected values."""
    try:
        return rfc8785.dumps(value)
    except (rfc8785.CanonicalizationError, TypeError, ValueError, UnicodeError) as exc:
        raise CanonicalizationError("value is not representable under RFC 8785 JCS") from None
