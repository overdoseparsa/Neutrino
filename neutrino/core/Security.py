# clery beacy 

from celery import shared_task
import secrets
import subprocess 

@shared_task(ignore_result=True) #TODO add The hasicorp value
def SECRET_KEY_CHANGE():
    new_secret_key = secrets.token_urlsafe(64)
    sed_command = f"sed -i 's/^SECRET_KEY=.*/SECRET_KEY={new_secret_key}/' .env && supervisorctl restart neutrino"
    subprocess.run(sed_command , shell=True , check=False)
