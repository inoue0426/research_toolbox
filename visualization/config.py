"""High-level defaults for publication-quality scientific figures."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Optional


@dataclass(frozen=True)
class FigureConfig:
    """Reusable defaults for publication figures.

    Typography is intentionally fixed at 10 pt by default so figures are
    consistent across scripts and remain easy to edit in Adobe Illustrator.
    Override only non-typographic properties unless there is a specific reason.
    """

    width_mm: float = 89.0
    aspect_ratio: float = 0.75
    font_family: str = "Arial"
    font_size: float = 10.0
    axes_linewidth: float = 0.8
    line_width: float = 1.2
    marker_size: float = 4.0
    tick_width: float = 0.8
    tick_length: float = 3.0
    raster_dpi: int = 600
    transparent: bool = False

    def with_updates(self, **kwargs) -> "FigureConfig":
        """Return a copy with selected values replaced."""
        return replace(self, **kwargs)


DEFAULT = FigureConfig()
SINGLE_COLUMN = FigureConfig(width_mm=89.0)
DOUBLE_COLUMN = FigureConfig(width_mm=178.0)


def resolve_config(config: Optional[FigureConfig] = None, **overrides) -> FigureConfig:
    """Resolve a config and optional per-call overrides."""
    base = config or DEFAULT
    valid = {key: value for key, value in overrides.items() if value is not None}
    return base.with_updates(**valid) if valid else base
