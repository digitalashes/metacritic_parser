FROM python:3-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/services/djangoapp/src
WORKDIR /opt/services/djangoapp/src

ADD config /opt/services/djangoapp/src/config
ADD project /opt/services/djangoapp/src/project
ADD manage.py /opt/services/djangoapp/src
ADD Pipfile /opt/services/djangoapp/src

RUN pip install -U pip wheel setuptools pipenv
RUN pipenv install --python /usr/local/bin/python3 --skip-lock

