# Started by copying the template from https://docs.docker.com/samples/django/
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code

# Doing this before /code/ avoids unnecessary re-runs of `pip install`
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/
