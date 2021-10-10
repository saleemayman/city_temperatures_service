#FROM ubuntu:latest
FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y python3-pip python3-dev libpq-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip


#EXPOSE 5000
WORKDIR /opt/web_app/

# copy all relevant files.
COPY . .
RUN pip install -r requirements.txt

# set app specific env variables
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1
ENV PYTHONIOENCODING=utf8

RUN chmod +x bin/start_app.sh


