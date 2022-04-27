Getting the Code
================

  git clone https://github.com/epixelnan/eps-keytrack.git

Setup
=====

  cd eps-keytrack/src
  make env-files

  make settings

Now edit keytrack/settings_private.py and keytrack/settings_secret.py.
Add 'localhost' to ALLOWED_HOSTS if you are deploying on your local machine.

Deploy
======

  sudo docker-compose up -d --build
  docker exec -it keytrack-web-con python manage.py check --deploy

Now set the superuser password for the Django admin app:

  docker exec -it keytrack-web-con python manage.py createsuperuser

Make sure to read:
https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

Usgae
=====
Visit localhost:8000 to use the site. You can submit registration requests
for regular users via localhost:8000/register/ and approve them after logging
in as the superuser.
