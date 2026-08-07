"""Matplotlib style helpers for publication figures and Adobe Illustrator editing."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator, Mapping, Optional, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt


MM_PER_INCH = 25.4


def mm_to_inches(*values_mm: float) -> float | Tuple[float, ...]:
    """Convert millimeters to inches.

    Parameters
    ----------
    *values_mm:
        One or more lengths in millimeters.

    Returns
    -------
    float or tuple[float, ...]
        Converted length(s) in inches.
    """
    converted = tuple(value / MM_PER_INCH for value in values_mm)
    return converted[0] if len(converted) == 1 else converted


def figure_size(width_mm: float = 89.0, aspect_ratio: float = 0.75) -> Tuple[float, float]:
    """Return a Matplotlib ``figsize`` in inches from a target width in mm.

    ``89 mm`` is a useful default for a single-column journal figure. Use a
    larger width such as ``178 mm`` for a double-column figure.
    """
    width_in = width_mm / MM_PER_INCH
    return width_in, width_in * aspect_ratio


def _illustrator_rc(
    *,
    font_family: str = "Arial",
    font_size: float = 8.0,
    axes_linewidth: float = 0.8,
    tick_width: float = 0.8,
    tick_length: float = 3.0,
) -> dict:
    """Build rcParams optimized for editable vector export."""
    return {
        # Typography
        "font.family": "sans-serif",
        "font.sans-serif": [font_family, "Helvetica", "DejaVu Sans"],
        "font.size": font_size,
        "axes.labelsize": font_size,
        "axes.titlesize": font_size,
        "xtick.labelsize": font_size,
        "ytick.labelsize": font_size,
        "legend.fontsize": font_size,
        # Keep text as text in PDF/PS instead of converting glyphs to paths.
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        # SVG text stays editable when opened in Illustrator.
        "svg.fonttype": "none",
        # Clean scientific-figure defaults.
        "axes.linewidth": axes_linewidth,
        "xtick.major.width": tick_width,
        "ytick.major.width": tick_width,
        "xtick.major.size": tick_length,
        "ytick.major.size": tick_length,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
    }


def set_illustrator_style(
    *,
    font_family: str = "Arial",
    font_size: float = 8.0,
    axes_linewidth: float = 0.8,
    tick_width: float = 0.8,
    tick_length: float = 3.0,
    extra_rc: Optional[Mapping[str, object]] = None,
) -> None:
    """Apply publication defaults globally to Matplotlib.

    Notes
    -----
    Matplotlib can only use Arial when it is installed on the system. The
    fallback list preserves a sans-serif appearance if Arial is unavailable.
    """
    rc = _illustrator_rc(
        font_family=font_family,
        font_size=font_size,
        axes_linewidth=axes_linewidth,
        tick_width=tick_width,
        tick_length=tick_length,
    )
    if extra_rc:
        rc.update(extra_rc)
    mpl.rcParams.update(rc)


@contextmanager
def illustrator_style(
    *,
    font_family: str = "Arial",
    font_size: float = 8.0,
    axes_linewidth: float = 0.8,
    tick_width: float = 0.8,
    tick_length: float = 3.0,
    extra_rc: Optional[Mapping[str, object]] = None,
) -> Iterator[None]:
    """Temporarily apply Illustrator-friendly Matplotlib settings."""
    rc = _illustrator_rc(
        font_family=font_family,
        font_size=font_size,
        axes_linewidth=axes_linewidth,
        tick_width=tick_width,
        tick_length=tick_length,
    )
    if extra_rc:
        rc.update(extra_rc)
    with mpl.rc_context(rc=rc):
        yield


def style_axis(
    ax: plt.Axes,
    *,
    despine: bool = True,
    tick_direction: str = "out",
    tick_width: float = 0.8,
    tick_length: float = 3.0,
) -> plt.Axes:
    """Apply a minimal publication style to an existing axis."""
    ax.tick_params(
        axis="both",
        which="major",
        direction=tick_direction,
        width=tick_width,
        length=tick_length,
    )
    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    return ax
