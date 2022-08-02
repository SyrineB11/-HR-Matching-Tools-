# Dockerfile

# pull the official docker image
FROM python:3.9.4-slim

# set work directory
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir -p /usr/share/man/man1

RUN apt update && apt install alembic -y

RUN apt-get update &&  apt-get install -y openjdk-11-jre-headless && apt-get clean;
RUN python3 -m spacy download en_core_web_sm;python3 -m spacy download en_core_web_lg

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
# copy project
COPY . .