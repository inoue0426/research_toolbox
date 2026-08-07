# Visualization Utilities

Helpers for making publication-quality Matplotlib figures that are easy to finish in **Adobe Illustrator**.

## Design goals

- Arial-first typography
- editable text in PDF/SVG exports
- vector-first output for lines, markers, and labels
- compact journal-style figure sizing
- minimal axis styling
- high-resolution raster fallback

## Recommended workflow

```python
import matplotlib.pyplot as plt

from visualization import figure_size, illustrator_style, save_figure

with illustrator_style(font_size=8):
    fig, ax = plt.subplots(figsize=figure_size(89, aspect_ratio=0.75))

    ax.plot(x, y)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Response")

    save_figure(fig, "figures/figure1")
```

This writes:

```text
figures/figure1.pdf
figures/figure1.svg
figures/figure1.png
```

## Illustrator compatibility

The style helper sets:

```python
pdf.fonttype = 42
ps.fonttype = 42
svg.fonttype = "none"
```

These settings are intended to preserve text as editable text rather than converting every glyph to a path.

For the most reliable Illustrator workflow:

1. Make sure **Arial is installed** on the machine generating the figure.
2. Export primarily as **PDF** or **SVG**.
3. Use PNG/TIFF only when a raster deliverable is required.
4. Avoid rasterizing artists unless necessary for very large scatter plots, heatmaps, or image-like layers.
5. Keep scientific labels, legends, and axis text in Matplotlib; make only final layout adjustments in Illustrator when possible.

## Figure widths

Useful starting points:

```python
figure_size(89)   # ~single-column figure
figure_size(178)  # ~double-column figure
```

The exact width requirements vary by journal, so treat these as convenient defaults rather than submission rules.

## Temporary vs global style

Temporary style is safer in notebooks:

```python
with illustrator_style():
    ...
```

For a script where all figures should share the same style:

```python
from visualization import set_illustrator_style

set_illustrator_style(font_size=8)
```

## Export only selected formats

```python
save_figure(
    fig,
    "figures/figure1",
    formats=("pdf", "svg"),
)
```

For raster-heavy figures:

```python
save_figure(
    fig,
    "figures/heatmap",
    formats=("pdf", "tiff"),
    dpi=600,
)
```
