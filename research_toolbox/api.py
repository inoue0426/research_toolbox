"""Convenience API for common research-toolbox operations.

Use this module when you want short, memorable function names. The underlying
modules remain available for advanced use and backwards compatibility.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping

from biomed import (
    UniProtClient,
    UniProtRecord,
    clean_text_for_matching,
    extract_pmc_sections,
    gene_to_uniprot as _gene_to_uniprot,
    genes_to_uniprot as _genes_to_uniprot,
    normalize_drug_name,
    normalize_gene_name,
    normalize_protein_name,
    uniprot_to_gene as _uniprot_to_gene,
    uniprots_to_gene as _uniprots_to_gene,
)
from caching import JSONFileCache, cached_lookup
from chemistry import smiles_to_morgan_fingerprint, smiles_to_morgan_fingerprints
from evaluation import compute_binary_metrics, summarize_binary_metrics
from reproducibility import seed_everything


def seed(value: int = 42, *, deterministic: bool = True) -> dict[str, Any]:
    """Seed Python, NumPy, and PyTorch when available."""
    return seed_everything(value, deterministic=deterministic)


def evaluate_binary(
    y_true: Iterable[int],
    y_score: Iterable[float],
    *,
    threshold: float = 0.5,
) -> dict[str, float]:
    """Evaluate binary probabilistic predictions."""
    return compute_binary_metrics(y_true, y_score, threshold=threshold)


def summarize_evaluations(results: Iterable[Mapping[str, float]]):
    """Summarize repeated metric dictionaries with mean/std/count."""
    return summarize_binary_metrics(results)


def fingerprint(smiles: str, **kwargs):
    """Create one Morgan fingerprint from a SMILES string."""
    return smiles_to_morgan_fingerprint(smiles, **kwargs)


def fingerprints(smiles: Iterable[str], **kwargs):
    """Create Morgan fingerprints for multiple SMILES strings."""
    return smiles_to_morgan_fingerprints(smiles, **kwargs)


def open_cache(path: str | Path = ".cache") -> JSONFileCache:
    """Open or create a JSON-backed cache directory."""
    return JSONFileCache(path)


def read_pmc(xml_path: str | Path, **kwargs) -> dict[str, str]:
    """Extract broad sections from a PMC/JATS XML article."""
    return extract_pmc_sections(xml_path, **kwargs)


def normalize_drug(value: str | None) -> str:
    """Normalize a drug name for lightweight matching/caching."""
    return normalize_drug_name(value)


def normalize_gene(value: str | None) -> str:
    """Normalize a gene symbol/name for lightweight matching/caching."""
    return normalize_gene_name(value)


def normalize_protein(value: str | None) -> str:
    """Normalize a protein name for lightweight matching/caching."""
    return normalize_protein_name(value)


def normalize_text(value: str | None) -> str:
    """Normalize free text for simple matching."""
    return clean_text_for_matching(value)


def gene_to_uniprot(
    gene: str,
    *,
    organism_id: int | None = 9606,
    reviewed: bool | None = True,
    all_matches: bool = False,
    client: UniProtClient | None = None,
):
    """Map a gene name to UniProtKB accession(s).

    Defaults to reviewed human entries because gene symbols are organism
    dependent. Override ``organism_id`` and ``reviewed`` when needed.
    """
    return _gene_to_uniprot(
        gene,
        organism_id=organism_id,
        reviewed=reviewed,
        all_matches=all_matches,
        client=client,
    )


def genes_to_uniprot(
    genes: Iterable[str],
    *,
    organism_id: int | None = 9606,
    reviewed: bool | None = True,
    all_matches: bool = False,
    client: UniProtClient | None = None,
):
    """Map multiple gene names to UniProtKB accession(s)."""
    return _genes_to_uniprot(
        genes,
        organism_id=organism_id,
        reviewed=reviewed,
        all_matches=all_matches,
        client=client,
    )


def uniprot_to_gene(accession: str, *, client: UniProtClient | None = None) -> str | None:
    """Map one UniProtKB accession to its primary gene name."""
    return _uniprot_to_gene(accession, client=client)


def uniprots_to_gene(
    accessions: Iterable[str],
    *,
    client: UniProtClient | None = None,
) -> dict[str, str | None]:
    """Map multiple UniProtKB accessions to primary gene names."""
    return _uniprots_to_gene(accessions, client=client)


__all__ = [
    "JSONFileCache",
    "UniProtClient",
    "UniProtRecord",
    "cached_lookup",
    "evaluate_binary",
    "fingerprint",
    "fingerprints",
    "gene_to_uniprot",
    "genes_to_uniprot",
    "normalize_drug",
    "normalize_gene",
    "normalize_protein",
    "normalize_text",
    "open_cache",
    "read_pmc",
    "seed",
    "summarize_evaluations",
    "uniprot_to_gene",
    "uniprots_to_gene",
]
