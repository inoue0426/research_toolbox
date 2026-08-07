"""Short visualization namespace.

Example
-------
>>> import research_toolbox as rt
>>> fig, ax = rt.viz.scatter(x, y, identity_line=True)
>>> rt.viz.save(fig, "figures/result")
"""

from visualization import (
    DEFAULT,
    DOUBLE_COLUMN,
    SINGLE_COLUMN,
    FigureConfig,
    add_panel_label,
    add_significance_bar,
    bar_plot,
    box_plot,
    figure_size,
    grouped_bar_plot,
    heatmap,
    illustrator_style,
    label_panels,
    line_plot,
    new_figure,
    save_figure,
    scatter_plot,
    set_illustrator_style,
    style_axis,
)

# Concise aliases for interactive use.
line = line_plot
scatter = scatter_plot
bar = bar_plot
grouped_bar = grouped_bar_plot
box = box_plot
save = save_figure
figure = new_figure
style = illustrator_style

__all__ = [
    "DEFAULT",
    "DOUBLE_COLUMN",
    "SINGLE_COLUMN",
    "FigureConfig",
    "add_panel_label",
    "add_significance_bar",
    "bar",
    "bar_plot",
    "box",
    "box_plot",
    "figure",
    "figure_size",
    "grouped_bar",
    "grouped_bar_plot",
    "heatmap",
    "illustrator_style",
    "label_panels",
    "line",
    "line_plot",
    "new_figure",
    "save",
    "save_figure",
    "scatter",
    "scatter_plot",
    "set_illustrator_style",
    "style",
    "style_axis",
]
