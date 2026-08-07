"""High-level plotting helpers for common scientific figures.

These functions intentionally return ``(fig, ax)`` instead of hiding Matplotlib,
so the result remains easy to customize before export.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

from .config import FigureConfig, resolve_config
from .style import figure_size, set_illustrator_style, style_axis


def _get_fig_ax(ax=None, *, config: FigureConfig | None = None, width_mm=None, aspect_ratio=None):
    cfg = resolve_config(config, width_mm=width_mm, aspect_ratio=aspect_ratio)
    set_illustrator_style(cfg)
    if ax is None:
        fig, ax = plt.subplots(figsize=figure_size(cfg.width_mm, cfg.aspect_ratio))
    else:
        fig = ax.figure
    style_axis(ax, config=cfg)
    return fig, ax, cfg


def line_plot(x, y, *, ax=None, label=None, xlabel=None, ylabel=None, title=None, config=None, **plot_kwargs):
    """Create a publication-ready line plot with minimal boilerplate."""
    fig, ax, _ = _get_fig_ax(ax, config=config)
    ax.plot(x, y, label=label, **plot_kwargs)
    _decorate(ax, xlabel=xlabel, ylabel=ylabel, title=title, legend=label is not None)
    return fig, ax


def scatter_plot(x, y, *, ax=None, xlabel=None, ylabel=None, title=None, identity_line=False, config=None, **scatter_kwargs):
    """Create a clean scatter plot, optionally with a y=x reference line."""
    fig, ax, _ = _get_fig_ax(ax, config=config)
    ax.scatter(x, y, **scatter_kwargs)
    if identity_line:
        finite_x = np.asarray(x, dtype=float)
        finite_y = np.asarray(y, dtype=float)
        values = np.concatenate([finite_x[np.isfinite(finite_x)], finite_y[np.isfinite(finite_y)]])
        if len(values):
            lo, hi = values.min(), values.max()
            ax.plot([lo, hi], [lo, hi], linestyle="--", linewidth=0.8)
    _decorate(ax, xlabel=xlabel, ylabel=ylabel, title=title)
    return fig, ax


def bar_plot(labels, values, *, errors=None, ax=None, xlabel=None, ylabel=None, title=None, horizontal=False, config=None, **bar_kwargs):
    """Create a compact bar plot for means, scores, or summary statistics."""
    fig, ax, _ = _get_fig_ax(ax, config=config)
    positions = np.arange(len(labels))
    if horizontal:
        ax.barh(positions, values, xerr=errors, **bar_kwargs)
        ax.set_yticks(positions, labels)
    else:
        ax.bar(positions, values, yerr=errors, **bar_kwargs)
        ax.set_xticks(positions, labels)
    _decorate(ax, xlabel=xlabel, ylabel=ylabel, title=title)
    return fig, ax


def grouped_bar_plot(labels, series: dict[str, Sequence[float]], *, ax=None, ylabel=None, title=None, config=None, group_width=0.8, **bar_kwargs):
    """Create grouped bars from ``{series_name: values}``."""
    fig, ax, _ = _get_fig_ax(ax, config=config)
    names = list(series)
    x = np.arange(len(labels))
    width = group_width / max(len(names), 1)
    start = -(len(names) - 1) * width / 2
    for i, name in enumerate(names):
        ax.bar(x + start + i * width, series[name], width=width, label=name, **bar_kwargs)
    ax.set_xticks(x, labels)
    _decorate(ax, ylabel=ylabel, title=title, legend=True)
    return fig, ax


def heatmap(matrix, *, ax=None, row_labels=None, col_labels=None, xlabel=None, ylabel=None, title=None, colorbar=True, colorbar_label=None, config=None, **imshow_kwargs):
    """Create a dependency-light heatmap using Matplotlib only."""
    fig, ax, _ = _get_fig_ax(ax, config=config)
    image = ax.imshow(matrix, aspect="auto", interpolation="nearest", **imshow_kwargs)
    if row_labels is not None:
        ax.set_yticks(np.arange(len(row_labels)), row_labels)
    if col_labels is not None:
        ax.set_xticks(np.arange(len(col_labels)), col_labels)
    if colorbar:
        cbar = fig.colorbar(image, ax=ax)
        if colorbar_label:
            cbar.set_label(colorbar_label)
    _decorate(ax, xlabel=xlabel, ylabel=ylabel, title=title)
    return fig, ax


def box_plot(data, *, labels: Optional[Sequence[str]] = None, ax=None, ylabel=None, title=None, show_points=False, config=None, **box_kwargs):
    """Create a box plot with optional raw-data overlay."""
    fig, ax, _ = _get_fig_ax(ax, config=config)
    ax.boxplot(data, labels=labels, **box_kwargs)
    if show_points:
        rng = np.random.default_rng(0)
        for i, values in enumerate(data, start=1):
            values = np.asarray(values)
            jitter = rng.normal(i, 0.035, size=len(values))
            ax.scatter(jitter, values, s=8, alpha=0.7)
    _decorate(ax, ylabel=ylabel, title=title)
    return fig, ax


def _decorate(ax, *, xlabel=None, ylabel=None, title=None, legend=False):
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
    if legend:
        ax.legend()
    return ax
