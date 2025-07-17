from celery import shared_task
import os 
from config.env import env

from django.utils.timezone import now



@shared_task
def postgress_backup(dir):
    try :
        backups_dir = dir + now().strftime('%d/%m/%Y') if '/' in dir else dir + '/' +now().strftime('%d/%m/%Y')
        os.system(f"pg_dump -U {env('DATABASE_USER',None)} -h {env('DATABASE_HOST',None)} -p {env('DATABASE_PORT',None)} {env('DATABASE_NAME',None)} > {backups_dir}")
    except BaseException as E:
        return False