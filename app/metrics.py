from typing import Any


METRICS_DATA: dict[str, Any] = {
    'requests_total': 0,
}


def increment_requests() -> dict[str, Any]:
    """Increment request counter.
    Args:
        None: No arguments."""
    METRICS_DATA['requests_total'] += 1
    return METRICS_DATA


def get_metrics() -> dict[str, Any]:
    """Return metrics data.
    Args:
        None: No arguments."""
    return METRICS_DATA
