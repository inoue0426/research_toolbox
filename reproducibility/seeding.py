"""Reproducibility helpers for Python, NumPy, and optionally PyTorch."""

from __future__ import annotations

import os
import random
from typing import Any

import numpy as np


def seed_everything(seed: int = 42, *, deterministic: bool = True) -> dict[str, Any]:
    """Seed common random-number generators.

    PyTorch is configured when installed; it is not a hard dependency of this
    module. Deterministic execution can reduce performance and does not guarantee
    bitwise reproducibility across different hardware/software stacks.
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)

    info: dict[str, Any] = {
        "seed": seed,
        "python": True,
        "numpy": True,
        "torch": False,
        "deterministic": deterministic,
    }

    try:
        import torch
    except ImportError:
        return info

    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

    if deterministic:
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        try:
            torch.use_deterministic_algorithms(True, warn_only=True)
        except (AttributeError, TypeError):
            pass

    info["torch"] = True
    info["torch_version"] = torch.__version__
    return info
