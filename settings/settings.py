import os
import logging
from lcogt_logging import LCOGTFormatter
from datetime import timedelta


# Logging configuration, can import and setup to use.
logConf = {
    "formatters": {
        "default": {
            "()": LCOGTFormatter
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        }
    },
    "loggers": {
        "ingester": {
            "handlers": ["console"],
            "level": logging.INFO,
            "propagate": False,
        }
    },
    "version": 1
}

# General settings
broker_url = os.getenv('BROKER_URL', 'memory://localhost')
FITS_BROKER = os.getenv('FITS_BROKER', 'memory://localhost')
API_ROOT = os.getenv('API_ROOT', 'http://localhost:8000/')
AUTH_TOKEN = os.getenv('AUTH_TOKEN', '')

# AWS Credentials and defaults
BUCKET = os.getenv('BUCKET', 'ingestertest')

# Files we wish to ignore
DISALLOWED_CHARS = ['-t00', '-x00', '-g00', '-l00', '-kb11', '-kb15', 'tstnrs']

# Fits headers we don't want to ingest
HEADER_BLACKLIST = ('HISTORY', 'COMMENT', '')

# Fits headers that must be present
REQUIRED_HEADERS = ('PROPID', 'DATE-OBS', 'INSTRUME', 'SITEID', 'TELID', 'OBSTYPE', 'BLKUID')

# Celery Settings
celery_config = {
    'broker_url': broker_url,
    'task_soft_time_limit': 1200,
    'task_time_limit': 3600,
    'worker_prefetch_multiplier': 1,
    'worker_max_tasks_per_child': 10,
    'beat_schedule': {
        'queue-length-every-minute': {
            'task': 'tasks.collect_queue_length_metric',
            'schedule': timedelta(minutes=1),
            'args': ('http://ingesterrabbitmq:15672/',),
            'options': {'queue': 'periodic'}
        },
        'total-holdings-every-5-minutes': {
            'task': 'tasks.total_holdings',
            'schedule': timedelta(minutes=5),
            'args': (API_ROOT, AUTH_TOKEN),
            'options': {'queue': 'periodic'}
        }
    }
}
