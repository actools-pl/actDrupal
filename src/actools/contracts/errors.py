"""Bounded, non-reflective errors for CP-002 data contracts."""

from __future__ import annotations


class ConfigurationError(ValueError):
    """Configuration parsing/validation failure with path and reason only."""

    def __init__(self, path: str, reason: str) -> None:
        self.path = path if path else "/"
        self.reason = reason
        super().__init__(f"configuration error at {self.path}: {self.reason}")


class CanonicalizationError(ValueError):
    """RFC 8785 canonicalization failure that does not reflect rejected data."""
