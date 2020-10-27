FROM python:3.8.2-slim

RUN apt-get update
RUN apt-get install git -y

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN mkdir /logs /uploads

WORKDIR /code

RUN pip install --upgrade pip
RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --dev --ignore-pipfile --system
