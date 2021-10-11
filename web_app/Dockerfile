#FROM ubuntu:latest
FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y python3-pip python3-dev libpq-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip

# get postgres client to enable app to connect to posgtres DB.
RUN apt-get update -qq && apt-get install postgresql-client -y

# install curl to test API calls from app container
RUN apt-get install curl -y

# set working directory for this app.
WORKDIR /opt/web_app/

# copy project files.
COPY . .
RUN pip install -r requirements.txt

# set app specific env variables
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1
ENV PYTHONIOENCODING=utf8

RUN chmod +x bin/wait_for_postgres.sh
#RUN chmod +x bin/start_app.sh


