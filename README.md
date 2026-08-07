# Research Toolbox

A personal collection of **reusable research utilities, analysis patterns, templates, and infrastructure**.

The goal of this repository is not to store project-specific code. It is to preserve components that are useful across multiple research projects and reduce repeated implementation work.

## Principles

1. **Reusable over project-specific** — add something here when it is useful beyond a single project.
2. **Small and composable** — prefer focused utilities over large frameworks.
3. **Reproducible by default** — utilities should make seeds, versions, splits, and assumptions explicit where relevant.
4. **Document the scientific intent** — explain what a tool is for, not only how it works.
5. **Promote only after reuse** — code can live in a project first; move/generalize it here after it proves useful.
6. **Prefer boring, dependable implementations** — research infrastructure should reduce uncertainty, not create it.

## Current Utilities

```text
research_toolbox/
├── biomed/
│   ├── normalization.py      # Lightweight drug/gene/protein string normalization
│   └── pmc_xml.py            # PubMed Central / JATS XML section extraction
├── caching/
│   ├── file_cache.py         # Atomic, JSON-backed file cache
│   └── lookup.py             # Generic cache-through lookup helper
├── chemistry/
│   └── fingerprints.py       # SMILES → Morgan fingerprints (RDKit)
├── evaluation/
│   └── classification.py     # Binary classification metrics and run summaries
├── reproducibility/
│   └── seeding.py            # Python / NumPy / optional PyTorch seeding
├── templates/
│   ├── benchmark.md
│   ├── experiment.md
│   └── project.md
└── README.md
```

The first utility set was generalized from reusable patterns in the public `drGT` and `DrugAgent` repositories rather than copied verbatim. Project-specific assumptions, paths, display code, and application-specific semantics were removed where possible.

### Design notes

- `evaluation/classification.py` separates metric computation from formatting and handles single-class AUROC explicitly.
- `reproducibility/seeding.py` treats PyTorch as optional and documents the limits of deterministic execution.
- `chemistry/fingerprints.py` makes invalid-SMILES behavior explicit (`raise`, `none`, or `zero`) instead of silently substituting a vector.
- `caching/file_cache.py` hashes keys to avoid filename collisions and writes atomically.
- `caching/lookup.py` can cache negative (`None`) lookups, which is useful for repeated API/database resolution.
- `biomed/normalization.py` is intentionally string normalization only; it is **not** entity resolution.
- `biomed/pmc_xml.py` performs heuristic section matching because PMC/JATS section names are not fully standardized.

## Optional Dependencies

Most modules use the Python standard library plus common scientific packages. Some utilities require optional packages:

- `evaluation/`: NumPy, pandas, scikit-learn
- `chemistry/`: NumPy, RDKit
- `reproducibility/`: NumPy; PyTorch is optional
- `caching/` and `biomed/`: standard library only

## What belongs here?

Good candidates:

- bootstrap confidence intervals used across projects
- repeated model-comparison code
- reproducible train/validation/test splitting
- gene identifier conversion helpers
- standard plotting functions
- SLURM array-job templates
- experiment and benchmark templates
- dataset validation checks
- small command-line utilities used across repositories

Usually **not** a good fit:

- a complete research project
- one-off exploratory notebooks
- raw or processed datasets
- project-specific configuration
- code whose assumptions are tightly coupled to one paper
- unreviewed snippets copied here only because they might be useful someday

## Promotion Rule

> **If I have implemented or copied this for a second research project, consider generalizing it. If I use it for a third, it probably belongs here.**

Before promoting code from a project:

- [ ] remove project-specific paths and constants
- [ ] make inputs and outputs explicit
- [ ] document assumptions
- [ ] add a minimal usage example
- [ ] handle obvious edge cases
- [ ] add a lightweight test when failure would silently affect scientific results

## Template Workflow

The templates in [`templates/`](templates/) are meant to make the reasoning behind experiments explicit *before* execution.

- [`experiment.md`](templates/experiment.md) — define a hypothesis, outcomes, and decision criteria before running an experiment
- [`benchmark.md`](templates/benchmark.md) — design fair model or method comparisons
- [`project.md`](templates/project.md) — initialize an executable research project from a selected idea

## Relationship to Other Research Repositories

```text
Paper reading / literature
        ↓
Research ideas
        ↓
Project repositories
        ↓
Repeated useful components
        ↓
Research toolbox
```

When a toolbox component materially changes, downstream projects should pin or record the version/commit they used when reproducibility matters.
