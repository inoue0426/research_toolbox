"""Publication-quality plotting helpers optimized for Adobe Illustrator workflows."""

from .annotations import add_panel_label, add_significance_bar, label_panels
from .config import DEFAULT, DOUBLE_COLUMN, SINGLE_COLUMN, FigureConfig
from .plots import bar_plot, box_plot, grouped_bar_plot, heatmap, line_plot, scatter_plot
from .save import export_figure, save_figure
from .style import figure_size, illustrator_style, mm_to_inches, new_figure, set_illustrator_style, style_axis

__all__ = [
    "DEFAULT",
    "DOUBLE_COLUMN",
    "SINGLE_COLUMN",
    "FigureConfig",
    "add_panel_label",
    "add_significance_bar",
    "bar_plot",
    "box_plot",
    "export_figure",
    "figure_size",
    "grouped_bar_plot",
    "heatmap",
    "illustrator_style",
    "label_panels",
    "line_plot",
    "mm_to_inches",
    "new_figure",
    "save_figure",
    "scatter_plot",
    "set_illustrator_style",
    "style_axis",
]
