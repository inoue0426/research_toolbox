"""Lightweight biomedical string normalization helpers.

These functions normalize strings for matching/caching only. They do *not*
perform biomedical entity resolution or map names to canonical identifiers.
"""

from __future__ import annotations

import re
from typing import Optional


def _collapse(value: Optional[str]) -> str:
    return " ".join(str(value).strip().split()) if value is not None else ""


def normalize_drug_name(drug: Optional[str]) -> str:
    """Normalize a drug-name string for case-insensitive matching."""
    return _collapse(drug).lower()


def normalize_gene_name(gene: Optional[str]) -> str:
    """Normalize a gene-symbol-like string for matching (uppercase only)."""
    return _collapse(gene).upper()


def normalize_protein_name(protein: Optional[str]) -> str:
    """Normalize a protein-name string for matching (uppercase only)."""
    return _collapse(protein).upper()


def clean_text_for_matching(text: Optional[str]) -> str:
    """Collapse whitespace and lowercase arbitrary text."""
    return re.sub(r"\s+", " ", (text or "").strip()).lower()
