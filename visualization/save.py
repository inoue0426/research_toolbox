"""Figure export helpers for publication and Adobe Illustrator workflows."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import matplotlib.pyplot as plt

from .config import FigureConfig

VECTOR_FORMATS = ("pdf", "svg")
RASTER_FORMATS = ("png", "tiff")


def save_figure(
    fig: plt.Figure,
    path: str | Path,
    *,
    formats: Sequence[str] = ("pdf", "svg", "png"),
    dpi: int | None = None,
    config: FigureConfig | None = None,
    transparent: bool | None = None,
    close: bool = False,
    bbox_inches: str = "tight",
    pad_inches: float = 0.02,
) -> list[Path]:
    """Save a figure in multiple Illustrator- and publication-friendly formats.

    PDF and SVG preserve vector objects and editable text. PNG/TIFF are useful
    for previews and raster-only submission systems.
    """
    cfg = config or FigureConfig()
    dpi = cfg.raster_dpi if dpi is None else dpi
    transparent = cfg.transparent if transparent is None else transparent

    base = Path(path)
    base.parent.mkdir(parents=True, exist_ok=True)
    requested = [fmt.lower().lstrip(".") for fmt in formats]
    if not requested:
        raise ValueError("At least one output format is required.")

    outputs: list[Path] = []
    for fmt in requested:
        output = base.with_suffix(f".{fmt}")
        kwargs = {
            "format": fmt,
            "bbox_inches": bbox_inches,
            "pad_inches": pad_inches,
            "transparent": transparent,
        }
        if fmt in RASTER_FORMATS or fmt in VECTOR_FORMATS:
            kwargs["dpi"] = dpi
        fig.savefig(output, **kwargs)
        outputs.append(output)

    if close:
        plt.close(fig)
    return outputs


def export_figure(fig: plt.Figure, path: str | Path, **kwargs) -> list[Path]:
    """Short alias for :func:`save_figure`."""
    return save_figure(fig, path, **kwargs)
