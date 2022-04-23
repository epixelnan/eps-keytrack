# Started by copying the template from https://docs.docker.com/samples/django/
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . /code/
WORKDIR /code
RUN pip install -r requirements.txt
