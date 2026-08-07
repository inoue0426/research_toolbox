# Research Toolbox API Reference

This page is the canonical human-readable inventory of the public APIs implemented in `research_toolbox`.

For everyday use:

```python
import research_toolbox as rt
```

The rendered web version is available at:

- https://inoue0426.github.io/research-toolbox/

## Top-level facade

| API | Purpose |
|---|---|
| `rt.seed(value=42, deterministic=True)` | Seed Python, NumPy, and PyTorch when available. |
| `rt.evaluate_binary(y_true, y_score, threshold=0.5)` | Compute binary-classification metrics. |
| `rt.summarize_evaluations(results)` | Aggregate repeated metric dictionaries. |
| `rt.fingerprint(smiles, **kwargs)` | One Morgan fingerprint. |
| `rt.fingerprints(smiles, **kwargs)` | Batch Morgan fingerprints. |
| `rt.open_cache(path='.cache')` | Open a JSON-backed persistent cache. |
| `rt.cached_lookup(cache, key, fetcher, cache_none=True)` | Cache-through lookup. |
| `rt.read_pmc(xml_path, **kwargs)` | Extract broad sections from PMC/JATS XML. |
| `rt.normalize_drug(value)` | Normalize a drug string. |
| `rt.normalize_gene(value)` | Normalize a gene string. |
| `rt.normalize_protein(value)` | Normalize a protein string. |
| `rt.normalize_text(value)` | Normalize free text. |
| `rt.gene_to_uniprot(gene, ...)` | Gene → UniProtKB accession(s). |
| `rt.genes_to_uniprot(genes, ...)` | Batch gene → UniProtKB mapping. |
| `rt.uniprot_to_gene(accession, ...)` | UniProtKB accession → primary gene name. |
| `rt.uniprots_to_gene(accessions, ...)` | Batch UniProtKB → gene mapping. |
| `rt.UniProtClient(...)` | Reusable UniProt REST client with retry/backoff and optional cache. |
| `rt.UniProtRecord` | Structured UniProt result record. |

## Gene ↔ UniProt

Default gene lookup is intentionally configured for the common case of reviewed human UniProtKB entries:

```python
rt.gene_to_uniprot('TP53')
# 'P04637'

rt.uniprot_to_gene('P04637')
# 'TP53'
```

Key options:

- `organism_id=9606` by default
- `reviewed=True` by default
- `all_matches=False` by default
- `reviewed=None` includes reviewed and unreviewed entries
- pass a shared `UniProtClient` for caching/reuse

```python
client = rt.UniProtClient(cache=rt.open_cache('.cache/uniprot'))
record = client.uniprot_to_record('P04637')
```

`UniProtRecord` exposes `accession`, `gene_name`, `entry_name`, `organism_id`, `reviewed`, and `protein_name`.

## Evaluation

Domain APIs:

- `evaluation.evaluate_binary`
- `evaluation.compute_binary_metrics`
- `evaluation.summarize_evaluations`
- `evaluation.summarize_binary_metrics`

`compute_binary_metrics` includes accuracy, balanced accuracy, precision, recall, specificity, F1, F2, G-mean, MCC, Cohen's kappa, Brier score, AUROC, AUPR, and log loss.

## Chemistry

Domain APIs:

- `chemistry.fingerprint`
- `chemistry.fingerprints`
- `chemistry.smiles_to_morgan_fingerprint`
- `chemistry.smiles_to_morgan_fingerprints`

Important options:

```python
rt.fingerprint(
    smiles,
    radius=2,
    n_bits=2048,
    use_chirality=True,
    on_error='raise',  # 'raise' | 'none' | 'zero'
)
```

RDKit is optional and only required for chemistry utilities.

## Caching

Domain APIs:

- `caching.JSONFileCache`
- `caching.open_cache`
- `caching.cached_lookup`

`JSONFileCache` supports:

- `get(key, default=None)`
- `set(key, value)`
- `get_or_set(key, fetcher, cache_none=True)`
- `contains(key)`
- `delete(key)`
- `clear()`
- `cache[key]`
- `cache[key] = value`
- `key in cache`
- `len(cache)`

## Biomedical text and normalization

Domain APIs:

- `biomed.read_pmc` / `biomed.extract_pmc_sections`
- `biomed.normalize_drug` / `biomed.normalize_drug_name`
- `biomed.normalize_gene` / `biomed.normalize_gene_name`
- `biomed.normalize_protein` / `biomed.normalize_protein_name`
- `biomed.normalize_text` / `biomed.clean_text_for_matching`
- `biomed.gene_to_uniprot`
- `biomed.genes_to_uniprot`
- `biomed.uniprot_to_gene`
- `biomed.uniprots_to_gene`
- `biomed.UniProtClient`
- `biomed.UniProtRecord`

The normalization helpers are lightweight string normalization, not entity resolution.

## Reproducibility

Domain APIs:

- `reproducibility.seed`
- `reproducibility.seed_everything`

Seeds Python, NumPy, and PyTorch/CUDA when PyTorch is installed.

## Visualization

Recommended short namespace:

```python
fig, ax = rt.viz.scatter(x, y)
rt.viz.save(fig, 'figures/result')
```

High-level plots:

- `rt.viz.line`
- `rt.viz.scatter`
- `rt.viz.bar`
- `rt.viz.grouped_bar`
- `rt.viz.box`
- `rt.viz.heatmap`

Configuration and layout:

- `FigureConfig`
- `DEFAULT`
- `SINGLE_COLUMN`
- `DOUBLE_COLUMN`
- `new_figure`
- `figure_size`
- `mm_to_inches`
- `illustrator_style`
- `set_illustrator_style`
- `style_axis`

Annotations:

- `add_panel_label`
- `label_panels`
- `add_significance_bar`

Export:

- `save_figure`
- `export_figure`
- `rt.viz.save`

Visualization defaults are designed for Adobe Illustrator handoff: Arial-first typography, PDF/PS Type 42 fonts, SVG text preserved as text, vector-first export, and high-resolution raster fallback.

## Maintenance rule

When a new public utility is added, update this file and the rendered page at `https://inoue0426.github.io/research-toolbox/` together with the relevant module `__all__` exports.
