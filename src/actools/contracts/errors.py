"""Bounded, non-reflective errors for versioned data contracts."""

from __future__ import annotations


class ConfigurationError(ValueError):
    """Configuration parsing/validation failure with path and reason only."""

    def __init__(self, path: str, reason: str) -> None:
        self.path = path if path else "/"
        self.reason = reason
        super().__init__(f"configuration error at {self.path}: {self.reason}")


class CanonicalizationError(ValueError):
    """RFC 8785 canonicalization failure that does not reflect rejected data."""


class ContractError(ValueError):
    """Contract parsing or validation failure with owned identifiers only."""

    def __init__(self, family: str, path: str, reason: str) -> None:
        self.family = family
        self.path = path if path else "/"
        self.reason = reason
        super().__init__(f"{family} contract error at {self.path}: {self.reason}")


class ContractVersionError(ContractError):
    """A reader was asked to accept an unsupported contract version."""


class RequirementGraphError(ContractError):
    """A requirement graph violates a source-owned semantic invariant."""

    def __init__(self, path: str, reason: str) -> None:
        super().__init__("requirement-graph", path, reason)


class EvaluationError(ValueError):
    """A pure diagnostic evaluation request is internally inconsistent."""
