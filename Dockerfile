FROM python:3.11.2-slim-buster

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1

#install system dependencies
RUN apt-get update \
 && apt-get -y install netcat gcc postgresql \
 && apt-get clean

COPY ./requirements.txt .
RUN pip install -r requirements.txt 

COPY . .
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh