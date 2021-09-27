FROM python:3.8.12-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/emerald:$PYTHONPATH

WORKDIR /emerald/

RUN pip install pipenv
COPY Pipfile* ./
RUN pipenv install --system

COPY . .

EXPOSE 5000