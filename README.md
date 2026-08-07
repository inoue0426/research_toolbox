# Research Toolbox

Reusable utilities for scientific computing, computational biology, and research workflows.

The repository has a **small convenience API** for everyday use while keeping domain modules available for advanced control.

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

### Biomedical utilities

```python
sections = rt.read_pmc("article.xml")

gene = rt.normalize_gene(" tp53 ")
drug = rt.normalize_drug("  Erlotinib  ")
protein = rt.normalize_protein("egfr")
text = rt.normalize_text("  Some   Text ")
```

Normalization is intentionally lightweight string normalization, **not biomedical entity resolution**.

#### Gene name ↔ UniProtKB

The common human, reviewed-entry case is one call:

```python
accession = rt.gene_to_uniprot("TP53")
# "P04637"

gene = rt.uniprot_to_gene("P04637")
# "TP53"
```

Batch lookup:

```python
gene_to_accession = rt.genes_to_uniprot(["TP53", "EGFR", "BRCA1"])
accession_to_gene = rt.uniprots_to_gene(["P04637", "P00533", "P38398"])
```

Gene symbols are organism-dependent, so the high-level API defaults to human (`organism_id=9606`). It also defaults to reviewed UniProtKB/Swiss-Prot entries:

```python
rt.gene_to_uniprot("Tp53", organism_id=10090)       # mouse
rt.gene_to_uniprot("TP53", reviewed=None)           # reviewed + unreviewed
rt.gene_to_uniprot("TP53", all_matches=True)        # all matching accessions
```

For repeated lookups, use a cached client:

```python
client = rt.UniProtClient(
    cache=rt.open_cache(".cache/uniprot")
)

accession = rt.gene_to_uniprot("TP53", client=client)
gene = rt.uniprot_to_gene("P04637", client=client)
```

For metadata rather than only the identifier:

```python
record = client.uniprot_to_record("P04637")
print(record.accession)
print(record.gene_name)
print(record.entry_name)
print(record.organism_id)
print(record.reviewed)
print(record.protein_name)
```

The implementation uses the public UniProt REST API and returns `None` for a valid query with no matching record. Network/API failures raise `RuntimeError` rather than being silently interpreted as missing biology.

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
from biomed import (
    gene_to_uniprot,
    normalize_gene,
    read_pmc,
    uniprot_to_gene,
)
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
├── biomed/                 # PMC XML, name normalization, UniProt mapping
├── caching/                # JSON cache + cache-through lookup
├── chemistry/              # Morgan fingerprints
├── evaluation/             # binary classification evaluation
├── reproducibility/        # seeding / deterministic execution helpers
├── visualization/          # Illustrator-friendly publication figures
├── templates/              # experiment / benchmark / project templates
└── pyproject.toml
```

## API design rules

1. **Short names for common tasks** — `seed`, `fingerprint`, `evaluate_binary`, `gene_to_uniprot`, `read_pmc`, `viz.scatter`.
2. **Long names remain available** — useful when explicitness matters.
3. **Scientific assumptions stay visible** — organism, review status, thresholds, invalid-input behavior, and deterministic settings remain configurable.
4. **Return standard Python/scientific objects** — dictionaries, arrays, DataFrames, and Matplotlib objects; small dataclasses are used only when structured metadata adds value.
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
