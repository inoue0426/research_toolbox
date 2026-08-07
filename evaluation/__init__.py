from .classification import compute_binary_metrics, summarize_binary_metrics

# Short public aliases.
evaluate_binary = compute_binary_metrics
summarize = summarize_binary_metrics

__all__ = [
    "compute_binary_metrics",
    "evaluate_binary",
    "summarize",
    "summarize_binary_metrics",
]
