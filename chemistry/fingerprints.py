"""Molecular fingerprint utilities built on RDKit.

Generalized from SMILES processing used in drGT. Failure behavior is explicit so
invalid molecules cannot silently become valid-looking vectors.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Literal

import numpy as np

ErrorMode = Literal["raise", "none", "zero"]


def _parse_smiles(smiles: str, *, use_chirality: bool = True):
    try:
        from rdkit import Chem
    except ImportError as exc:
        raise ImportError("RDKit is required for chemistry.fingerprints") from exc

    params = Chem.SmilesParserParams()
    params.sanitize = True
    params.useChirality = use_chirality
    params.removeHs = False
    mol = Chem.MolFromSmiles(smiles, params=params)
    if mol is not None:
        return mol

    # Fallback for structures that fail full sanitization.
    params.sanitize = False
    mol = Chem.MolFromSmiles(smiles, params=params)
    if mol is None:
        return None
    try:
        Chem.SanitizeMol(mol, Chem.SANITIZE_ALL ^ Chem.SANITIZE_PROPERTIES)
    except Exception:
        return None
    return mol


def smiles_to_morgan_fingerprint(
    smiles: str,
    *,
    radius: int = 2,
    n_bits: int = 2048,
    use_chirality: bool = True,
    on_error: ErrorMode = "raise",
) -> np.ndarray | None:
    """Convert one SMILES string to a Morgan bit-vector as a NumPy array."""
    if on_error not in {"raise", "none", "zero"}:
        raise ValueError("on_error must be one of: 'raise', 'none', 'zero'")
    if not isinstance(smiles, str) or not smiles.strip():
        mol = None
    else:
        mol = _parse_smiles(smiles, use_chirality=use_chirality)

    if mol is None:
        if on_error == "none":
            return None
        if on_error == "zero":
            return np.zeros(n_bits, dtype=np.uint8)
        raise ValueError(f"Could not parse SMILES: {smiles!r}")

    try:
        from rdkit.Chem import rdFingerprintGenerator

        generator = rdFingerprintGenerator.GetMorganGenerator(radius=radius, fpSize=n_bits)
        fp = generator.GetFingerprint(mol)
    except (ImportError, AttributeError):
        from rdkit.Chem import AllChem

        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)

    return np.asarray(fp, dtype=np.uint8)


def smiles_to_morgan_fingerprints(
    smiles: Iterable[str],
    **kwargs,
) -> np.ndarray | list[np.ndarray | None]:
    """Convert multiple SMILES strings while preserving input order.

    When ``on_error='none'`` the return value is a list because failed entries are
    represented by ``None``. Otherwise a 2-D NumPy array is returned.
    """
    items = [smiles_to_morgan_fingerprint(s, **kwargs) for s in smiles]
    if kwargs.get("on_error", "raise") == "none":
        return items
    return np.stack(items)
