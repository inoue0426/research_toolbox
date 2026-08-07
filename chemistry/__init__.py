from .fingerprints import smiles_to_morgan_fingerprint, smiles_to_morgan_fingerprints

fingerprint = smiles_to_morgan_fingerprint
fingerprints = smiles_to_morgan_fingerprints

__all__ = [
    "fingerprint",
    "fingerprints",
    "smiles_to_morgan_fingerprint",
    "smiles_to_morgan_fingerprints",
]
