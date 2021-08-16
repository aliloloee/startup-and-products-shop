FROM python:3.9
LABEL MAINTAINER="Ali Loloee Jahromi"

ENV PYTHONUNBUFFERED 1

RUN mkdir /startup
WORKDIR /startup
COPY . /startup

ADD requirements.txt /startup
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput
