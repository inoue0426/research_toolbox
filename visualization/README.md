# Visualization Utilities

A small, opinionated wrapper around Matplotlib for **publication figures that remain easy to edit in Adobe Illustrator**.

The package is intentionally high-level for common plots, but it always returns normal Matplotlib ``fig``/``ax`` objects so nothing is locked away.

## Defaults

- Arial-first typography
- editable text in PDF/SVG (`pdf.fonttype=42`, `ps.fonttype=42`, `svg.fonttype='none'`)
- journal-friendly physical widths (89 mm single column, 178 mm double column)
- minimal axes and outward ticks
- vector-first PDF/SVG export plus 600 dpi raster fallback
- no forced color palette: choose colors explicitly when the scientific context requires them

## Fastest workflow

```python
from visualization import scatter_plot, save_figure

fig, ax = scatter_plot(
    y_true,
    y_pred,
    xlabel="Observed",
    ylabel="Predicted",
    identity_line=True,
)
save_figure(fig, "figures/model_performance")
```

## Reusable configuration

```python
from visualization import FigureConfig, scatter_plot, save_figure

paper = FigureConfig(
    width_mm=89,
    font_size=8,
    marker_size=3.5,
)

fig, ax = scatter_plot(x, y, config=paper)
save_figure(fig, "figures/figure1", config=paper)
```

Built-in presets:

```python
from visualization import SINGLE_COLUMN, DOUBLE_COLUMN
```

Use ``config.with_updates(...)`` to change only one property.

## Common plots

```python
from visualization import (
    line_plot,
    scatter_plot,
    bar_plot,
    grouped_bar_plot,
    box_plot,
    heatmap,
)
```

All return ``(fig, ax)``. Pass an existing ``ax=...`` when composing panels.

### Line

```python
fig, ax = line_plot(x, y, xlabel="Epoch", ylabel="Loss")
```

### Scatter

```python
fig, ax = scatter_plot(x, y, identity_line=True)
```

### Bar

```python
fig, ax = bar_plot(["A", "B", "C"], means, errors=stds)
```

### Grouped bars

```python
fig, ax = grouped_bar_plot(
    ["Dataset 1", "Dataset 2"],
    {"Baseline": baseline, "Model": model},
    ylabel="AUROC",
)
```

### Box plot

```python
fig, ax = box_plot(values, labels=["A", "B"], show_points=True)
```

### Heatmap

```python
fig, ax = heatmap(
    matrix,
    row_labels=genes,
    col_labels=drugs,
    colorbar_label="Score",
)
```

## Multi-panel figures

```python
from visualization import DOUBLE_COLUMN, illustrator_style, label_panels
import matplotlib.pyplot as plt

with illustrator_style(DOUBLE_COLUMN):
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
    # plot into axes[0], axes[1]
    label_panels(axes)
```

Individual labels are also available:

```python
from visualization import add_panel_label, add_significance_bar

add_panel_label(ax, "A")
add_significance_bar(ax, 0, 1, y=1.1, text="p < 0.01")
```

## Lower-level control

For custom plots that are not covered by the wrappers:

```python
from visualization import new_figure, style_axis

fig, ax = new_figure()
ax.plot(...)
style_axis(ax)
```

Or use a temporary style context:

```python
from visualization import illustrator_style

with illustrator_style(font_size=7):
    ...
```

## Export

```python
from visualization import save_figure

save_figure(fig, "figures/figure1")
```

Default output:

```text
figure1.pdf
figure1.svg
figure1.png
```

PDF/SVG are the preferred Illustrator handoff formats. PNG/TIFF are mainly for previews and raster-only submission systems.

## Design rule

These helpers should remove repetitive formatting code, not replace Matplotlib. If a plot needs specialized scientific encoding, create the plot normally and use the shared style/export helpers around it.
