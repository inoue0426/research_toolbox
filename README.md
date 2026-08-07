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

## Structure

```text
research_toolbox/
├── bioinformatics/     # Gene IDs, expression matrices, pathways, omics utilities
├── evaluation/        # Metrics, confidence intervals, statistical comparisons
├── ml/                # Reproducibility, splits, training/evaluation helpers
├── visualization/     # Reusable research plotting utilities
├── slurm/             # SLURM scripts and HPC patterns
├── templates/         # Experiment, benchmark, and project templates
└── README.md
```

The structure is intentionally minimal. Add subdirectories only when there is a concrete reusable artifact to put in them.

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

## Promotion rule

A practical rule for deciding whether code should move here:

> **If I have implemented or copied this for a second research project, consider generalizing it. If I use it for a third, it probably belongs here.**

Before promoting code from a project:

- [ ] remove project-specific paths and constants
- [ ] make inputs and outputs explicit
- [ ] document assumptions
- [ ] add a minimal usage example
- [ ] handle obvious edge cases
- [ ] add a lightweight test when failure would silently affect scientific results

## Template workflow

The templates in [`templates/`](templates/) are meant to make the reasoning behind experiments explicit *before* execution.

- [`experiment.md`](templates/experiment.md) — define a hypothesis, outcomes, and decision criteria before running an experiment
- [`benchmark.md`](templates/benchmark.md) — design fair model or method comparisons
- [`project.md`](templates/project.md) — initialize an executable research project from a selected idea

## Relationship to other research repositories

This repository should contain **reusable execution infrastructure**.

A useful separation is:

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
