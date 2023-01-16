FROM python:3.10

WORKDIR /app

COPY src/requirements.txt /app/requirements.txt
COPY ./objects /app/objects

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

COPY src /app/src
