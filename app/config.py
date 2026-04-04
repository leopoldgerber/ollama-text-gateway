import os
from dotenv import load_dotenv

load_dotenv()


def get_env_value(env_name: str, default_value: str) -> str:
    """Get environment value.
    Args:
        env_name (str): Environment variable name.
        default_value (str): Fallback value."""
    env_value = os.getenv(env_name, default_value)
    return env_value


def get_required_env(env_name: str) -> str:
    """Get required environment value.
    Args:
        env_name (str): Environment variable name."""
    env_value = os.getenv(env_name)
    if not env_value:
        raise ValueError(f'{env_name} is missing')
    return env_value


def build_settings() -> dict[str, str]:
    """Build application settings.
    Args:
        None: No arguments."""
    settings_data = {
        'app_title': get_env_value(
            env_name='APP_TITLE',
            default_value='Ollama Text Gateway',
        ),
        'app_host': get_env_value(
            env_name='APP_HOST',
            default_value='0.0.0.0',
        ),
        'app_port': get_env_value(
            env_name='APP_PORT',
            default_value='8000',
        ),
        'app_reload': get_env_value(
            env_name='APP_RELOAD',
            default_value='true',
        ),
        'ollama_api_key': get_required_env(env_name='OLLAMA_API_KEY'),
        'ollama_base_url': get_env_value(
            env_name='OLLAMA_BASE_URL',
            default_value='https://ollama.com',
        ),
        'ollama_model_name': get_env_value(
            env_name='OLLAMA_MODEL_NAME',
            default_value='gpt-oss:20b-cloud',
        ),
        'log_level': get_env_value(
            env_name='LOG_LEVEL',
            default_value='INFO',
        ),
        'log_dir': get_env_value(
            env_name='LOG_DIR',
            default_value='logs',
        ),
        'log_file_name': get_env_value(
            env_name='LOG_FILE_NAME',
            default_value='app.log',
        ),
        'metrics_path': get_env_value(
            env_name='METRICS_PATH',
            default_value='/metrics',
        ),
        'metrics_json_path': get_env_value(
            env_name='METRICS_JSON_PATH',
            default_value='/metrics/json',
        ),
        'prometheus_multiproc_dir': get_env_value(
            env_name='PROMETHEUS_MULTIPROC_DIR',
            default_value='',
        ),
    }
    return settings_data


SETTINGS = build_settings()
