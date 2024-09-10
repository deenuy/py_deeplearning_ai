import logging
import os
from datetime import datetime
from logging.config import dictConfig
from typing import Optional, Dict, Any

from api.utils.config import ConfigLoader

def setup_logger(
        config_path: str,
        logger_name: str,
        log_level: str = 'INFO',
        custom_formatters: Optional[Dict[str, Dict[str, Any]]] = None,
        custom_filters: Optional[Dict[str, Dict[str, Any]]] = None
) -> None:
    """
    Set up logging using a structured configuration from a YAML file, including correlation ID support and log rotation.

    Args:
        config_path (str): Path to the configuration YAML file.
        logger_name (str): Name of the logger. Defaults to 'app_logger'.
        log_level (str): Log level to set for the logger. Defaults to 'INFO'.
        custom_formatters (Optional[Dict[str, Dict[str, Any]]]): Custom formatters to add or override.
        custom_filters (Optional[Dict[str, Dict[str, Any]]]): Custom filters to add or override.

    Raises:
        FileNotFoundError: If the config file is not found.
        KeyError: If required configuration keys are missing.
        OSError: If there's an error creating the log directory.

    Usage:
        setup_logger(logger_name='my_project')
        logger = logging.getLogger('my_project')
        logger.info("Application started with enhanced logging.")
    """
    try:
        # Load configuration
        config_loader = ConfigLoader(config_path)
        config = config_loader.load_config()

        log_dir = config['logs']['dir']
        os.makedirs(log_dir, exist_ok=True)

        # Set log file name with a timestamp for uniqueness
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_file_name = os.path.join(log_dir, f"{config['logs']['fname']}-{timestamp}.log")

        # Base logging configuration
        log_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'filters': {
                'correlation_id': {
                    '()': 'asgi_correlation_id.CorrelationIdFilter',
                    'uuid_length': 32,
                    'default_value': '-',
                },
            },
            'formatters': {
                'console': {
                    'class': 'logging.Formatter',
                    'format': '%(levelname)s:\t%(asctime)s %(name)s:%(lineno)d [%(correlation_id)s] [%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s',
                    "datefmt": "%Y-%m-%d %H:%M:%S"
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'filters': ['correlation_id'],
                    'formatter': 'console',
                },
                'file': {
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'level': config['logs'].get('level', log_level).upper(),
                    'formatter': 'console',
                    'filename': log_file_name,
                    'when': config['logs'].get('when', 'midnight'),
                    'interval': config['logs'].get('interval', 1),
                    'backupCount': config['logs'].get('backup_count', 15),
                    'filters': ['correlation_id'],
                },
            },
            'loggers': {
                logger_name: {
                    'handlers': ['file', 'console'],
                    'level': config['logs'].get('level', log_level).upper(),
                    'propagate': False
                },
            },
        }

        # Add custom formatters and filters if provided
        if custom_formatters:
            log_config['formatters'].update(custom_formatters)
        if custom_filters:
            log_config['filters'].update(custom_filters)

        dictConfig(log_config)

        # Override the log record factory for customized log processing
        old_factory = logging.getLogRecordFactory()

        def record_factory(*args, **kwargs):
            record = old_factory(*args, **kwargs)
            record.msg = str(record.msg).replace("\n", "<N>")
            return record

        logging.setLogRecordFactory(record_factory)

    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except KeyError as e:
        raise KeyError(f"Missing required configuration key: {str(e)}")
    except OSError as e:
        raise OSError(f"Error creating log directory: {str(e)}")


# Example usage
if __name__ == "__main__":
    setup_logger('py-log-fname', 'config/dev/config.yml', level='DEBUG')
    logger = logging.getLogger('example_logger')
    logger.info("Logging setup complete.")
    logger.debug("This is a debug message.")
    logger.warning("This is a warning message.")
    try:
        1 / 0
    except Exception as e:
        logger.exception("An error occurred:")