"""Annotations and panel-label helpers for multi-panel scientific figures."""

from __future__ import annotations

from string import ascii_uppercase
from typing import Iterable, Sequence

import matplotlib.pyplot as plt


def add_panel_label(
    ax: plt.Axes,
    label: str,
    *,
    x: float = -0.12,
    y: float = 1.05,
    fontsize: float | None = None,
    fontweight: str = "bold",
    **text_kwargs,
):
    """Add a panel label such as ``A`` or ``B`` in axes coordinates."""
    kwargs = {
        "transform": ax.transAxes,
        "ha": "left",
        "va": "bottom",
        "fontweight": fontweight,
        "clip_on": False,
    }
    if fontsize is not None:
        kwargs["fontsize"] = fontsize
    kwargs.update(text_kwargs)
    return ax.text(x, y, label, **kwargs)


def label_panels(
    axes: Iterable[plt.Axes],
    *,
    labels: Sequence[str] | None = None,
    start: int = 0,
    **kwargs,
) -> list:
    """Label multiple axes sequentially using A, B, C, ... by default."""
    axes = list(axes)
    if labels is None:
        labels = list(ascii_uppercase[start : start + len(axes)])
    if len(labels) != len(axes):
        raise ValueError("Number of labels must match number of axes.")
    return [add_panel_label(ax, label, **kwargs) for ax, label in zip(axes, labels)]


def add_significance_bar(
    ax: plt.Axes,
    x1: float,
    x2: float,
    y: float,
    text: str,
    *,
    height: float = 0.02,
    linewidth: float = 0.8,
    text_offset: float = 0.01,
):
    """Add a simple significance bracket between two x positions."""
    ax.plot([x1, x1, x2, x2], [y, y + height, y + height, y], linewidth=linewidth, clip_on=False)
    return ax.text((x1 + x2) / 2, y + height + text_offset, text, ha="center", va="bottom")
