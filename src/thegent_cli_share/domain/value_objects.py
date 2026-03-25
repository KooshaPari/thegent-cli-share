"""Domain value objects - immutable objects defined by their attributes.

Value Object Principles:
- Immutable (no setters, create new instances)
- No identity (two VOs with same values are equal)
- Self-validating
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass(frozen=True)
class CommandHash:
    """Immutable command hash for deduplication."""
    value: str
    algorithm: str = "sha256"

    def __str__(self) -> str:
        return self.value

    def __len__(self) -> int:
        return len(self.value)


@dataclass(frozen=True)
class TaskMetadata:
    """Immutable task metadata."""
    command: str
    cwd: str
    env: tuple[tuple[str, str], ...]
    timeout_seconds: int = 3600

    def with_timeout(self, seconds: int) -> "TaskMetadata":
        """Create new TaskMetadata with different timeout."""
        return TaskMetadata(
            command=self.command,
            cwd=self.cwd,
            env=self.env,
            timeout_seconds=seconds,
        )


@dataclass(frozen=True)
class MergeConflict:
    """Immutable merge conflict information."""
    file_path: str
    line_start: int
    line_end: int
    ours_content: str
    theirs_content: str

    @property
    def conflict_range(self) -> str:
        return f"{self.line_start}-{self.line_end}"


@dataclass(frozen=True)
class HealthScore:
    """Health score for system monitoring."""
    overall: float
    components: tuple[tuple[str, float], ...]

    @classmethod
    def from_components(cls, **kwargs: float) -> "HealthScore":
        """Create health score from components."""
        components = tuple(kwargs.items())
        if not components:
            return cls(overall=1.0, components=())
        overall = sum(v for _, v in components) / len(components)
        return cls(overall=overall, components=components)

    def is_healthy(self) -> bool:
        return self.overall >= 0.8

    def is_degraded(self) -> bool:
        return 0.5 <= self.overall < 0.8

    def is_unhealthy(self) -> bool:
        return self.overall < 0.5
