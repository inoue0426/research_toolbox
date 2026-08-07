"""Figure export helpers for publication and Adobe Illustrator workflows."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import matplotlib.pyplot as plt


VECTOR_FORMATS = ("pdf", "svg")
RASTER_FORMATS = ("png", "tiff")


def save_figure(
    fig: plt.Figure,
    path: str | Path,
    *,
    formats: Sequence[str] = ("pdf", "svg", "png"),
    dpi: int = 600,
    transparent: bool = False,
    close: bool = False,
    bbox_inches: str = "tight",
    pad_inches: float = 0.02,
) -> list[Path]:
    """Save one figure in multiple publication-friendly formats.

    Parameters
    ----------
    fig:
        Matplotlib figure to export.
    path:
        Output path with or without a suffix. For example ``figures/fig1`` or
        ``figures/fig1.pdf``. When multiple formats are requested, the suffix
        is replaced for each output format.
    formats:
        Output formats. PDF and SVG are recommended for Illustrator because
        vector objects and text remain editable when the backend supports it.
        PNG/TIFF are useful for previews or raster-only submission systems.
    dpi:
        Resolution used for raster output and rasterized artists embedded in
        otherwise-vector figures.
    transparent:
        Save with a transparent background.
    close:
        Close the figure after export.

    Returns
    -------
    list[pathlib.Path]
        Paths written to disk.
    """
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
