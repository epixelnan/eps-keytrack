Please see README.txt from the parent directory to know how to get this
app deployed.

The project was started on 2021-12-22 by following the
instructions found on https://docs.docker.com/samples/django/

You don't have to run `./manage.py makemigrations` unless you make changes
to the models. If doing so, it is usually done on the host machine, not
inside the container. On Ubuntu/Debian, run `apt install libpq-dev` to get
pg_config, if reported missing by `pip install`.
