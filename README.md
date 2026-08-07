# Research Toolbox

Reusable utilities for scientific computing, computational biology, and research workflows.

The repository now has a **small convenience API** for everyday use while keeping domain modules available for advanced control.

## Install

```bash
pip install -e .
```

Optional extras:

```bash
pip install -e '.[evaluation]'
pip install -e '.[chemistry]'
pip install -e '.[visualization]'
pip install -e '.[all]'
```

## Recommended API

```python
import research_toolbox as rt
```

### Reproducibility

```python
rt.seed(42)
```

### Evaluation

```python
metrics = rt.evaluate_binary(y_true, y_prob)
summary = rt.summarize_evaluations(all_runs)
```

### Chemistry

```python
fp = rt.fingerprint(smiles)
fps = rt.fingerprints(smiles_list)
```

Invalid-SMILES behavior remains explicit:

```python
rt.fingerprint(smiles, on_error="raise")  # default
rt.fingerprint(smiles, on_error="none")
rt.fingerprint(smiles, on_error="zero")
```

### Cache

```python
cache = rt.open_cache(".cache")

cache["result"] = {"score": 0.91}
result = cache["result"]

value = cache.get_or_set(
    "expensive-query",
    lambda: expensive_function(),
)
```

The standalone cache-through helper is also available:

```python
value = rt.cached_lookup(cache, "key", fetcher)
```

### Biomedical text

```python
sections = rt.read_pmc("article.xml")

gene = rt.normalize_gene(" tp53 ")
drug = rt.normalize_drug("  Erlotinib  ")
protein = rt.normalize_protein("egfr")
text = rt.normalize_text("  Some   Text ")
```

Normalization is intentionally lightweight string normalization, **not biomedical entity resolution**.

### Visualization

Use the short `viz` namespace:

```python
fig, ax = rt.viz.scatter(
    y_true,
    y_pred,
    xlabel="Observed",
    ylabel="Predicted",
    identity_line=True,
)

rt.viz.save(fig, "figures/prediction")
```

Other common wrappers:

```python
rt.viz.line(...)
rt.viz.bar(...)
rt.viz.grouped_bar(...)
rt.viz.box(...)
rt.viz.heatmap(...)
```

All plotting helpers return normal Matplotlib `(fig, ax)` objects, so customization remains unrestricted.

Publication defaults are optimized for an Adobe Illustrator workflow:

- Arial-first typography
- editable PDF/SVG text
- PDF/PS Type 42 fonts
- SVG text preserved as text
- 89 mm single-column and 178 mm double-column presets
- vector-first export with 600 dpi raster fallback

```python
paper = rt.viz.FigureConfig(
    width_mm=89,
    font_size=8,
    marker_size=3.5,
)

fig, ax = rt.viz.scatter(x, y, config=paper)
rt.viz.save(fig, "figures/figure1", config=paper)
```

## Domain APIs

The concise API is optional. Existing domain imports remain supported:

```python
from evaluation import evaluate_binary
from chemistry import fingerprint
from caching import open_cache
from biomed import read_pmc, normalize_gene
from reproducibility import seed
from visualization import scatter, save
```

Long-form function names remain available as well, for example `compute_binary_metrics`, `smiles_to_morgan_fingerprint`, and `seed_everything`.

## Structure

```text
research_toolbox/
├── research_toolbox/       # compact public facade (`import research_toolbox as rt`)
│   ├── api.py
│   └── viz.py
├── biomed/                 # PMC XML + biomedical string normalization
├── caching/                # JSON cache + cache-through lookup
├── chemistry/              # Morgan fingerprints
├── evaluation/             # binary classification evaluation
├── reproducibility/        # seeding / deterministic execution helpers
├── visualization/          # Illustrator-friendly publication figures
├── templates/              # experiment / benchmark / project templates
└── pyproject.toml
```

## API design rules

1. **Short names for common tasks** — `seed`, `fingerprint`, `evaluate_binary`, `read_pmc`, `viz.scatter`.
2. **Long names remain available** — useful when explicitness matters.
3. **No hidden scientific assumptions** — thresholds, invalid-input behavior, and deterministic settings remain configurable.
4. **Return standard Python/scientific objects** — dictionaries, arrays, DataFrames, and Matplotlib objects rather than custom wrappers unless they add clear value.
5. **Optional heavy dependencies** — RDKit, Matplotlib, scikit-learn, and PyTorch are only needed for the modules that use them.
6. **Backwards compatible where practical** — existing module-level APIs remain usable while the facade provides a cleaner default.

## Promotion rule

> If a utility is useful across multiple research projects, generalize it here; if it is tightly coupled to one scientific project, keep it in that project.

Before promoting code:

- remove project-specific paths and constants
- expose explicit inputs and outputs
- document assumptions
- handle obvious failure modes
- add tests when silent failure could affect scientific conclusions

## Templates

- `templates/experiment.md` — hypothesis, expected outcomes, interpretation, and go/no-go criteria
- `templates/benchmark.md` — fair model/method comparison design
- `templates/project.md` — turn a selected research idea into an executable project
