from typing import Any

from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client import CollectorRegistry
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Histogram
from prometheus_client import REGISTRY
from prometheus_client import generate_latest
from prometheus_client import multiprocess

from app.config import SETTINGS


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

REQUEST_COUNT = Counter(
    'ollama_text_gateway_requests_total',
    'Total number of processed requests.',
    ['endpoint'],
)

ERROR_COUNT = Counter(
    'ollama_text_gateway_errors_total',
    'Total number of processed errors.',
    ['error_type'],
)

REQUEST_TIME = Histogram(
    'ollama_text_gateway_request_duration_seconds',
    'Request processing duration.',
    ['endpoint'],
)

HEALTH_STATUS = Gauge(
    'ollama_text_gateway_health_status',
    'Service health status.',
)


def increment_requests(endpoint: str) -> dict[str, Any]:
    """Increment request counter.
    Args:
        endpoint (str): Request endpoint."""
    METRICS_DATA['requests_total'] += 1
    REQUEST_COUNT.labels(endpoint=endpoint).inc()
    return METRICS_DATA


def increment_errors(error_type: str) -> dict[str, Any]:
    """Increment error counters.
    Args:
        error_type (str): Error metric field name."""
    METRICS_DATA['errors_total'] += 1

    if error_type in METRICS_DATA:
        METRICS_DATA[error_type] += 1

    ERROR_COUNT.labels(error_type=error_type).inc()
    return METRICS_DATA


def save_response_time(
    endpoint: str,
    response_time: float,
) -> dict[str, Any]:
    """Save response time metrics.
    Args:
        endpoint (str): Request endpoint.
        response_time (float): Request processing time."""
    METRICS_DATA['last_response_time_seconds'] = response_time
    METRICS_DATA['response_time_total_seconds'] += response_time
    METRICS_DATA['response_time_count'] += 1

    total_time = METRICS_DATA['response_time_total_seconds']
    total_count = METRICS_DATA['response_time_count']

    average_time = total_time / total_count
    METRICS_DATA['average_response_time_seconds'] = average_time

    REQUEST_TIME.labels(endpoint=endpoint).observe(response_time)
    return METRICS_DATA


def update_health(status_value: int) -> Gauge:
    """Update health gauge.
    Args:
        status_value (int): Health status value."""
    HEALTH_STATUS.set(status_value)
    return HEALTH_STATUS


def get_metrics() -> dict[str, Any]:
    """Return metrics data.
    Args:
        None: No arguments."""
    return METRICS_DATA


def get_registry() -> CollectorRegistry | Any:
    """Build metrics registry.
    Args:
        None: No arguments."""
    multiproc_dir = SETTINGS['prometheus_multiproc_dir']

    if multiproc_dir:
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
        return registry

    return REGISTRY


def get_metrics_output() -> bytes:
    """Build Prometheus metrics output.
    Args:
        None: No arguments."""
    registry = get_registry()
    metrics_output = generate_latest(registry)
    return metrics_output


def get_metrics_type() -> str:
    """Return metrics content type.
    Args:
        None: No arguments."""
    return CONTENT_TYPE_LATEST
