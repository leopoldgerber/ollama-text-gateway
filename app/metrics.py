from typing import Any


METRICS_DATA: dict[str, Any] = {
    'requests_total': 0,
    'errors_total': 0,
    'validation_errors_total': 0,
    'ollama_connection_errors_total': 0,
    'ollama_response_errors_total': 0,
    'last_response_time_seconds': 0.0,
    'response_time_total_seconds': 0.0,
    'response_time_count': 0,
    'average_response_time_seconds': 0.0,
}


def increment_requests() -> dict[str, Any]:
    """Increment request counter.
    Args:
        None: No arguments."""
    METRICS_DATA['requests_total'] += 1
    return METRICS_DATA


def increment_errors(error_type: str) -> dict[str, Any]:
    """Increment error counters.
    Args:
        error_type (str): Error metric field name."""
    METRICS_DATA['errors_total'] += 1

    if error_type in METRICS_DATA:
        METRICS_DATA[error_type] += 1

    return METRICS_DATA


def save_response_time(response_time: float) -> dict[str, Any]:
    """Save response time metrics.
    Args:
        response_time (float): Request processing time."""
    METRICS_DATA['last_response_time_seconds'] = response_time
    METRICS_DATA['response_time_total_seconds'] += response_time
    METRICS_DATA['response_time_count'] += 1

    total_time = METRICS_DATA['response_time_total_seconds']
    total_count = METRICS_DATA['response_time_count']

    average_time = total_time / total_count
    METRICS_DATA['average_response_time_seconds'] = average_time

    return METRICS_DATA


def get_metrics() -> dict[str, Any]:
    """Return metrics data.
    Args:
        None: No arguments."""
    return METRICS_DATA
