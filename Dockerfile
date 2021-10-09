FROM ubuntu:latest

RUN apt-get update \
    && apt-get install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip

#EXPOSE 5000
WORKDIR /opt/work/

COPY requirements.txt .
RUN pip install -r requirements.txt

# copy relevant files
COPY bin/ bin/
COPY app.py .
COPY config.py .
COPY models.py .
COPY setup.py .

RUN chmod +x bin/start_app.sh


