"""Reusable binary-classification evaluation utilities.

Generalized from evaluation code used in drGT. Metric computation is kept
separate from display/formatting so the functions are safe to reuse in scripts,
notebooks, hyperparameter searches, and tests.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    cohen_kappa_score,
    f1_score,
    fbeta_score,
    log_loss,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)


def _as_1d(values: Iterable[float]) -> np.ndarray:
    arr = np.asarray(values).reshape(-1)
    return arr


def compute_binary_metrics(
    y_true: Iterable[int],
    y_score: Iterable[float],
    *,
    threshold: float = 0.5,
) -> dict[str, float]:
    """Compute common metrics for binary probabilistic predictions.

    Parameters
    ----------
    y_true:
        Binary ground-truth labels (0/1).
    y_score:
        Predicted probabilities or scores in [0, 1].
    threshold:
        Threshold used to convert scores to hard labels.

    Notes
    -----
    AUROC is undefined when only one class is present. In that case the value is
    returned as ``nan`` rather than raising. The same principle is used for
    metrics whose mathematical definition is unavailable for the supplied data.
    """
    true = _as_1d(y_true)
    score = _as_1d(y_score).astype(float)
    if true.shape != score.shape:
        raise ValueError(f"Shape mismatch: y_true={true.shape}, y_score={score.shape}")
    if true.size == 0:
        raise ValueError("y_true and y_score must not be empty")
    if not np.isin(true, [0, 1]).all():
        raise ValueError("y_true must contain only binary labels 0 and 1")
    if not np.isfinite(score).all():
        raise ValueError("y_score must contain only finite values")
    if np.any((score < 0) | (score > 1)):
        raise ValueError("y_score must be in [0, 1]")

    pred = (score >= threshold).astype(int)
    recall = recall_score(true, pred, zero_division=0)
    specificity = recall_score(true, pred, pos_label=0, zero_division=0)

    metrics: dict[str, float] = {
        "accuracy": accuracy_score(true, pred),
        "balanced_accuracy": balanced_accuracy_score(true, pred),
        "precision": precision_score(true, pred, zero_division=0),
        "recall": recall,
        "specificity": specificity,
        "f1": f1_score(true, pred, zero_division=0),
        "f2": fbeta_score(true, pred, beta=2, zero_division=0),
        "g_mean": float(np.sqrt(recall * specificity)),
        "mcc": matthews_corrcoef(true, pred),
        "cohen_kappa": cohen_kappa_score(true, pred),
        "brier": brier_score_loss(true, score),
    }

    # Probability metrics with class-dependent definitions.
    if np.unique(true).size == 2:
        metrics["auroc"] = roc_auc_score(true, score)
        metrics["aupr"] = average_precision_score(true, score)
        metrics["log_loss"] = log_loss(true, score, labels=[0, 1])
    else:
        metrics["auroc"] = float("nan")
        metrics["aupr"] = float("nan")
        metrics["log_loss"] = log_loss(true, score, labels=[0, 1])

    return metrics


def summarize_binary_metrics(
    results: Iterable[Mapping[str, float]],
) -> pd.DataFrame:
    """Summarize repeated metric dictionaries with mean, std, and valid count."""
    frame = pd.DataFrame(list(results), dtype=float)
    if frame.empty:
        raise ValueError("results must contain at least one metric mapping")
    return pd.DataFrame(
        {
            "mean": frame.mean(skipna=True),
            "std": frame.std(skipna=True),
            "n": frame.count(),
        }
    )
