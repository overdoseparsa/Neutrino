from config.env import env

# https://docs.celeryproject.org/en/stable/userguide/configuration.html

CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='amqp://guest:guest@localhost//')
CELERY_RESULT_BACKEND = 'django-db' # TODO add to redis  
CELERY_TIMEZONE = 'UTC'

CELERY_TASK_SOFT_TIME_LIMIT = 20  # seconds
CELERT_TASK_TIME_LIMIT = 30  # seconds
CELERY_TASK_MAX_RETRIES = 3
from neutrino.core.backups import postgress_backup
CELERY_BEAT_SCHEDULE = {
    'notify_customers': {
        'task': 'config.tasks.notify_customers',
        'schedule': 500,
        'args': ['Hello World'],
    } , 
    'postgres_backup': {
        'task': 'neutrino.core.backups.postgress_backup',
        'schedule': 500,
        'args': [env('DIR_BACKOPS',default=None)],
    }, 
    'Reload_secert_key': {
        'task': 'neutrino.core.Security.SECRET_KEY_CHANGE',
        'schedule': 2592000   } # one month 
}