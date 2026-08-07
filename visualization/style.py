"""Matplotlib style helpers for publication figures and Adobe Illustrator editing."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator, Mapping, Optional, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt

from .config import FigureConfig, resolve_config

MM_PER_INCH = 25.4


def mm_to_inches(*values_mm: float) -> float | Tuple[float, ...]:
    converted = tuple(value / MM_PER_INCH for value in values_mm)
    return converted[0] if len(converted) == 1 else converted


def figure_size(width_mm: float = 89.0, aspect_ratio: float = 0.75) -> Tuple[float, float]:
    width_in = width_mm / MM_PER_INCH
    return width_in, width_in * aspect_ratio


def _illustrator_rc(config: FigureConfig, extra_rc: Optional[Mapping[str, object]] = None) -> dict:
    rc = {
        "font.family": "sans-serif",
        "font.sans-serif": [config.font_family, "Helvetica", "DejaVu Sans"],
        "font.size": config.font_size,
        "axes.labelsize": config.font_size,
        "axes.titlesize": config.font_size,
        "xtick.labelsize": config.font_size,
        "ytick.labelsize": config.font_size,
        "legend.fontsize": config.font_size,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "axes.linewidth": config.axes_linewidth,
        "lines.linewidth": config.line_width,
        "lines.markersize": config.marker_size,
        "xtick.major.width": config.tick_width,
        "ytick.major.width": config.tick_width,
        "xtick.major.size": config.tick_length,
        "ytick.major.size": config.tick_length,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "figure.dpi": 150,
        "savefig.dpi": config.raster_dpi,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
    }
    if extra_rc:
        rc.update(extra_rc)
    return rc


def set_illustrator_style(config: Optional[FigureConfig] = None, *, extra_rc=None, **overrides) -> FigureConfig:
    """Apply Illustrator-friendly publication defaults globally and return the resolved config."""
    resolved = resolve_config(config, **overrides)
    mpl.rcParams.update(_illustrator_rc(resolved, extra_rc))
    return resolved


@contextmanager
def illustrator_style(config: Optional[FigureConfig] = None, *, extra_rc=None, **overrides) -> Iterator[FigureConfig]:
    """Temporarily apply Illustrator-friendly defaults.

    Yields the resolved :class:`FigureConfig`, so callers can reuse its values.
    """
    resolved = resolve_config(config, **overrides)
    with mpl.rc_context(rc=_illustrator_rc(resolved, extra_rc)):
        yield resolved


def style_axis(ax: plt.Axes, *, config: Optional[FigureConfig] = None, despine: bool = True, grid: bool = False) -> plt.Axes:
    resolved = config or FigureConfig()
    ax.tick_params(axis="both", which="major", direction="out", width=resolved.tick_width, length=resolved.tick_length)
    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    if grid:
        ax.grid(axis="y", linewidth=0.5, alpha=0.25)
    return ax


def new_figure(*, config: Optional[FigureConfig] = None, width_mm: float | None = None, aspect_ratio: float | None = None, nrows: int = 1, ncols: int = 1, squeeze: bool = True, **subplot_kwargs):
    """Create a styled figure using journal-friendly physical dimensions."""
    resolved = resolve_config(config, width_mm=width_mm, aspect_ratio=aspect_ratio)
    set_illustrator_style(resolved)
    figsize = figure_size(resolved.width_mm, resolved.aspect_ratio)
    return plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, squeeze=squeeze, **subplot_kwargs)
